# Bachelor Thesis: Evolving Drums
Generating evolving drum sequences: A bachelor thesis provided by Sven Paqué (Leiden University) It contains all the code and generated MIDI files that is used for the research.

This Github contains all the generated MIDI files from each model and also some self-made audio that contain the generated drums with different samples.

# Appendix
Both models have a few limitations regarding their data input. This is not documented in the Magenta space.
Drums RNN only takes in Drum tracks that are specifically assigned to Channel 10 (the MIDI standard channel for drums). Otherwise the model doesn't register the MIDI files and can't infer from them. We have used an old program called Aria Maestosa to change the remaining MIDI files that weren't already programmed to Channel 10.

MusicVAE handles the note pitch to drum instrument mapping itself. Unlike Drums RNN it doesn't use the General MIDI Drum Map, so you won't have to set each MIDI file to Channel 10. But it does have a limiting set of drum instruments that it can use. For example, a Hand Clap is registered as note pitch 39 and MusicVAE doesn't have a mapping of note pitch 39 to a Hand Clap. Whenever you use a Hand Clap in your MIDI file, MusicVAE won't be able to handle it and therefore the model will fail.
To combat this problem, we have written another Python script which redefines all the note pitches that MusicVAE doesn't recognize, to note pitches that MusicVAE does recognize. It does mean however that with MusicVAE you can use less instrument heavy data than with DrumsRNN.

The Python scripts are inspired by the book Hands On With Magenta, and then carefully adjusted for our needs. They are in our Github under the folder Scripts.
Both models were trained by using Magenta commands in Ubuntu 20, we have defined an own config for Magenta to allow for longer sequences.

