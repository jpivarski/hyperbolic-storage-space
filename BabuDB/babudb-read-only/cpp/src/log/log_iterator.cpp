// Copyright (c) 2008, Felix Hupfeld, Jan Stender, Bjoern Kolbeck, Mikael Hoegqvist, Zuse Institute Berlin.
// Licensed under the BSD License, see LICENSE file for details.

#include "babudb/log/log_iterator.h"
#include "babudb/log/log_section.h"
#include "babudb/log/sequential_file.h"

#include "log/log_section_iterator.h"

#include "yield/platform/yunit.h"

#include <vector>

namespace babudb {

LogIterator::LogIterator(LogSectionIterator* current_section)
  : current_section(current_section) {}

LogIterator::~LogIterator() {}  // for auto_ptr

LogIterator* LogIterator::First(LogSectionIterator* first_section) {
  LogIterator* it = new LogIterator(first_section);
  if (first_section->IsValid()) {
    it->record_iterator = (**first_section)->First();
  }
  return it;
}

LogIterator* LogIterator::Last(LogSectionIterator* last_section) {
  LogIterator* it = new LogIterator(last_section);
  if (last_section->IsValid()) {
    it->record_iterator = (**last_section)->Last();
  }
  return it;
}

bool LogIterator::GetNext() {
  if (!record_iterator.GetNext()) {
    if (!current_section->GetNext()) {
      return false;
    } else {
      record_iterator = (**current_section)->First();
      return GetNext();
    }
  } else {
    ASSERT_TRUE(record_iterator.IsValid());
    return true;
  }
}

bool LogIterator::GetPrevious() {
  if (!record_iterator.GetPrevious()) {
    if (!current_section->GetPrevious()) {
      return false;
    } else {
      record_iterator = (**current_section)->Last();
      return GetPrevious();
    }
  } else {
    ASSERT_TRUE(record_iterator.IsValid());
    return true;
  }
}

bool LogIterator::IsValid() const {
  return record_iterator.IsValid();
}

bool LogIterator::operator != (const LogIterator& other) const {
  return *current_section != *other.current_section || record_iterator != other.record_iterator;
}

bool LogIterator::operator == (const LogIterator& other) const {
  return *current_section == *other.current_section && record_iterator == other.record_iterator;
}

Buffer LogIterator::operator * () const {
  return record_iterator.AsData();
}

Buffer LogIterator::GetOperationWithFrame() const {
  return Buffer(record_iterator.GetRecord(), record_iterator.GetRecord()->GetRecordSize());
}

}
