// This file is part of babudb/cpp
//
// Copyright (c) 2008, Felix Hupfeld, Jan Stender, Bjoern Kolbeck, Mikael Hoegqvist, Zuse Institute Berlin.
// Copyright (c) 2009, Felix Hupfeld
// Licensed under the BSD License, see LICENSE file for details.
//
// Author: Felix Hupfeld (felix@storagebox.org)

#include "babudb/log/log.h"

#include "babudb/log/log_iterator.h"
#include "babudb/log/log_section.h"
#include "babudb/log/log_storage.h"
#include "babudb/test.h"

#include "util.h"
#include "log/log_section_iterator.h"

#include <algorithm>
#include <sstream>
using namespace std;

#include "yield/platform/directory_walker.h"
using namespace yield;

namespace babudb {

Log::Log(Buffer data) : tail(NULL), name_prefix("") {  // volatile in-memory
  LogStorage* storage = new VolatileLogStorage(data);
  tail = new LogSection(storage, 1);
  sections.push_back(tail);
}

Log::Log(const string& name_prefix) : tail(NULL), name_prefix(name_prefix) {}

Log::~Log() {
  Close();
}

void Log::Close() {
  AdvanceTail();
  for(vector<LogSection*>::iterator i = sections.begin(); i != sections.end(); ++i) {
    delete *i;
  }
  sections.clear();
}

class LSNBefore {
public:
  typedef pair<yield::Path, lsn_t> vector_entry;
  bool operator () (const vector_entry& l, const vector_entry& r) { return l.second < r.second; }
};

typedef vector< pair<yield::Path, lsn_t> > DiskSections;

static DiskSections scanAvailableLogSections(const string& name_prefix) {
  DiskSections result;

  pair<yield::Path,yield::Path> prefix_parts = yield::Path(name_prefix).split();
  yield::DirectoryWalker walker(prefix_parts.first);

  while(walker.hasNext()) {
    lsn_t lsn;
    auto_ptr<yield::DirectoryEntry> entry = walker.getNext();

    if(matchFilename(entry->getPath(), prefix_parts.second.getHostCharsetPath(), "log", lsn))
      result.push_back(make_pair(entry->getPath(), lsn));
  }

  std::sort(result.begin(),result.end(),LSNBefore());
  return result;
}

// Rename log sections with LSNs smaller than to_lsn
void Log::Cleanup(lsn_t to_lsn, const string& obsolete_prefix) {
  DiskSections disk_sections = scanAvailableLogSections(name_prefix);  // sorted by LSN

  for (DiskSections::iterator i = disk_sections.begin(); i != disk_sections.end(); ++i) {
    DiskSections::iterator next = i; ++next;

    if (next != disk_sections.end() && next->second <= to_lsn) {
      pair<yield::Path,yield::Path> parts = i->first.split();
      yield::DiskOperations::rename(i->first, obsolete_prefix + parts.second.getHostCharsetPath());
    }
  }
}

// Loads all log sections with LSNs larger than min_lsn. Load them in order and check
// for continuity.
void Log::Open(lsn_t min_lsn) {
  ASSERT_TRUE(sections.size() == 0);  // otherwise somebody called startup() twice
  DiskSections disk_sections = scanAvailableLogSections(name_prefix);  // sorted by LSN

  for (DiskSections::iterator i = disk_sections.begin(); i != disk_sections.end(); ++i) {
    DiskSections::iterator next = i; ++next;

    if(next == disk_sections.end() || (min_lsn + 1) < next->second) {
      LogStorage* file = PersistentLogStorage::OpenReadOnly(i->first);
      LogSection* section = new LogSection(file, i->second);  // repairs if not graceful

      if (!section->empty()) {  // check if there is a LSN in this section
        sections.push_back(section);
      } else {
        delete section;
      }
    }
  }
}

LogSection* Log::GetTail(babudb::lsn_t next_lsn) {
  if(tail == NULL) {
    LogStorage* storage = NULL;
    // TODO: hack, refactor!
    if (!name_prefix.empty()) {
      std::ostringstream section_name;
      section_name << name_prefix << "_" << next_lsn << ".log";
      storage = PersistentLogStorage::Open(section_name.str());
    } else {
      storage = new VolatileLogStorage(1024);
    }
    tail = new LogSection(storage, next_lsn);
    sections.push_back(tail);
  }

  return tail;
}

void Log::AdvanceTail() {
  if (tail) {
    if (tail->isWritable()) {
      tail->truncate();
    }
  }
  tail = NULL;
}

int Log::NumberOfSections() const {
  return sections.size();
}

Log::iterator* Log::First() const {
  return LogIterator::First(LogSectionIterator::First(&sections));
}

Log::iterator* Log::Last() const {
  return LogIterator::Last(LogSectionIterator::Last(&sections));
}

}
