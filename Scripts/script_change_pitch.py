"""
Change pitches of drums for MusicVAE model

VERSION: Magenta 2.1.2
"""
import argparse
import copy
import glob
import math
import os
import random
import shutil
import timeit
from itertools import cycle
from multiprocessing import Manager
from multiprocessing.pool import Pool
from typing import List
from typing import Optional

import matplotlib.pyplot as plt
from pretty_midi import Instrument
from pretty_midi import PrettyMIDI

from multiprocessing_utils import AtomicCounter

parser = argparse.ArgumentParser()
parser.add_argument("--sample_size", type=int)
parser.add_argument("--pool_size", type=int, default=4)
parser.add_argument("--path_dataset_dir", type=str, required=True)
parser.add_argument("--path_output_dir", type=str, required=True)
args = parser.parse_args()

# The list of all MIDI paths on disk (we might process only a sample)
MIDI_PATHS = glob.glob(os.path.join(args.path_dataset_dir, "**", "*.mid"),
                       recursive=True)


def extract_drums(midi_path: str) -> Optional[PrettyMIDI]:
  """
  Extracts a PrettyMIDI instance of all the merged drum tracks
  from the given MIDI path.

  :param midi_path: the path to the MIDI file
  :return: the PrettyMIDI instance of the merged drum tracks
  """
  os.makedirs(args.path_output_dir, exist_ok=True)
  pm = PrettyMIDI(midi_path)
  return pm


def change_pitch_for_mv(pm_drums: PrettyMIDI) -> float:
  """
  Returns the ratio of the bass drums that fall directly on a beat.

  :param pm_drums: the PrettyMIDI instance to analyse
  :return: the ratio of the bass drums that fall on a beat
  """
  for note in pm_drums.instruments[0].notes:
      if note.pitch == 28 or note.pitch == 64 or note.pitch == 73 or note.pitch == 69 or note.pitch == 62 or note.pitch == 83 or note.pitch == 82 or note.pitch==81 or  note.pitch == 69:
        note.pitch = 42
      if note.pitch == 35:
        note.pitch = 36
      if note.pitch == 39:
        note.pitch = 38
      if note.pitch == 41 or note.pitch == 54:
        note.pitch = 42
      if note.pitch == 70:
        note.pitch = 71
      

def process(midi_path: str, counter: AtomicCounter) -> Optional[dict]:
  """
  Processes the MIDI file at the given path and increments the counter. The
  method will call the extract_drums method and the get_bass_drums_on_beat
  method, and write the resulting drum file if the bass drum ratio is over
  the threshold.

  :param midi_path: the MIDI file path to process
  :param counter: the counter to increment
  :return: the dictionary containing the MIDI path, the PrettyMIDI instance
  and the ratio of bass drum on beat, raises an exception if the file cannot
  be processed
  """
  try:
    pm_drums = extract_drums(midi_path)
    change_pitch_for_mv(pm_drums)
    midi_filename = os.path.basename(midi_path)
    pm_drums.write(os.path.join(args.path_output_dir, f"{midi_filename}.mid"))
    return {"midi_path": midi_path,
            "pm_drums": pm_drums}
  finally:
    counter.increment()


def app(midi_paths: List[str]):
  start = timeit.default_timer()

  # Cleanup the output directory
  shutil.rmtree(args.path_output_dir, ignore_errors=True)

  # Starts the threads
  with Pool(args.pool_size) as pool:
    manager = Manager()
    counter = AtomicCounter(manager, len(midi_paths), 1000)
    print("START")
    results = pool.starmap(process, zip(midi_paths, cycle([counter])))
    results = [result for result in results if result]
    print("END")
    results_percentage = len(results) / len(midi_paths) * 100
    print(f"Number of tracks: {len(MIDI_PATHS)}, "
          f"number of tracks in sample: {len(midi_paths)}, "
          f"number of results: {len(results)} "
          f"({results_percentage:.2f}%)")

  # Creates an histogram for the drum lengths
  pm_drums = [result["pm_drums"] for result in results]
  pm_drums_lengths = [pm.get_end_time() for pm in pm_drums]
  plt.figure(num=None, figsize=(10, 8), dpi=500)
  plt.hist(pm_drums_lengths, bins=100, color="darkmagenta")
  plt.title('Drums lengths')
  plt.ylabel('length (sec)')
  #plt.savefig('drum-length.png')

  stop = timeit.default_timer()
  print("Time: ", stop - start)


if __name__ == "__main__":
  print(args.path_dataset_dir)
  print(MIDI_PATHS)
  print(list(MIDI_PATHS))
  print(args.sample_size)
  if args.sample_size:
    # Process a sample of it
    MIDI_PATHS_SAMPLE = random.sample(list(MIDI_PATHS), args.sample_size)
  else:
    # Process all the dataset
    MIDI_PATHS_SAMPLE = list(MIDI_PATHS)
  app(MIDI_PATHS_SAMPLE)
