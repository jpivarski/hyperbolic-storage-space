// This file is part of babudb/cpp
//
// Copyright (c) 2008, Felix Hupfeld, Jan Stender, Bjoern Kolbeck, Mikael Hoegqvist, Zuse Institute Berlin.
// Copyright (c) 2009, Felix Hupfeld
// Licensed under the BSD License, see LICENSE file for details.
//
// Author: Felix Hupfeld (felix@storagebox.org)

#include "merged_index.h"

#include "babudb/log/log.h"
#include "babudb/log/log_section.h"
#include "babudb/lookup_iterator.h"
#include "babudb/key.h"
#include "log_index.h"
#include "index/index.h"

#include <algorithm>
#include <vector>
using std::vector;

#include "yield/platform/path.h"
#include "yield/platform/assert.h"
using namespace yield;

namespace babudb {

MergedIndex::MergedIndex(const std::string& name, const KeyOrder& order) 
    : tail(NULL), immutable_index(NULL), name_prefix(name), order(order)  {
  ImmutableIndex::DiskIndices indices = ImmutableIndex::FindIndices(name);
  immutable_index = ImmutableIndex::LoadLatestIntactIndex(indices, order);

  tail = new LogIndex(order, GetLastPersistentLSN());
  log_indices.push_back(tail);
}

MergedIndex::~MergedIndex() {
  delete immutable_index;

  for(vector<LogIndex*>::iterator i = log_indices.begin(); i != log_indices.end(); ++i)
    delete *i;
}

lsn_t MergedIndex::GetLastPersistentLSN() {
  if (immutable_index)
    return immutable_index->GetLastLSN();
  else
    return 0;
}

void MergedIndex::Add(const Buffer& key, const Buffer& value) {
  ASSERT_TRUE(key.isValidData() && !key.isEmpty());
  ASSERT_TRUE(value.isValidData());
  tail->Add(key, value);
}

void MergedIndex::Remove(const Buffer& key) {
  ASSERT_TRUE(key.isValidData() && !key.isEmpty());
  tail->Add(key, Buffer::Deleted());
}

Buffer MergedIndex::Lookup(const Buffer& key) {
  for (vector<LogIndex*>::iterator i = log_indices.begin();
       i != log_indices.end(); ++i) {
    Buffer result = (*i)->lookup(key);
    if (result.isNotExists()) {
      continue;
    } else if (result.isDeleted()) {
      return Buffer::NotExists();
    } else {
      return result;
    }
  }

  if (immutable_index) {
    return immutable_index->Lookup(key);
  }

  return Buffer::NotExists();
}

LookupIterator MergedIndex::Lookup(const Buffer& lower, const Buffer& upper) {
  return LookupIterator(log_indices, immutable_index, order, lower, upper);
}

void MergedIndex::Cleanup(const std::string& to) {
  if (immutable_index) {
    immutable_index->CleanupObsolete(name_prefix, to);
  }
}

void MergedIndex::Snapshot(lsn_t current_lsn) {
  tail = new LogIndex(order, current_lsn);
  log_indices.insert(log_indices.begin(), tail);
}

LookupIterator MergedIndex::GetSnapshot(lsn_t snapshot_lsn) {
  // Find and keep all indices up to the snapshot_lsn. Make sure that
  // there is actually a snapshot at lsn.
  bool found_snapshot = false;
  vector<LogIndex*> indices_up_to_snapshot;
  for(vector<LogIndex*>::iterator i = log_indices.begin();
    i != log_indices.end(); ++i) {
      if ((*i)->getFirstLSN() == snapshot_lsn) {
        found_snapshot = true;
      }
      
      if ((*i)->getFirstLSN() < snapshot_lsn) {
         ASSERT_TRUE(found_snapshot);
        indices_up_to_snapshot.push_back(*i);
      }
  }

  ASSERT_TRUE(found_snapshot);

  return LookupIterator(
      indices_up_to_snapshot, immutable_index, order);
}

}
