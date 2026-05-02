# Just Notes To Self

Whenever I think of something to improve but don't need another rabit hole, it goes here.

- [x] Combine the header and title bar rendering together
- [ ] Rendering the bank account can be a single renderer function
- [ ] Import all the src.screens files at once, maybe with the init py file?
- [ ] Look into pre-commit and pre-commmit-ci and dependabot
- [x] Lock window to 160x160, but have a scale int that allows for 2x, 3x, 4x, etc. scaling
  - [ ] Need to also have some sort of scaling for the font
- [ ] AsyncIO to update all planets while player is interacting with the current planet
- [ ] Have the core functionality and backend code in src/core?

- [ ] ~~Create a dict of pygame shortcuts in the interface init file~~
- [ ] ~~Maybe a nicer way of even spacing that doesn't rely on i = 0 loops~~
- [ ] ~~Header is universal height, could be a constant for alignment use~~
- [ ] ~~Maybe have state -> corestates -> gamestates where the core states are just the BSYW states that share the button bar~~
- [ ] ~~Make a single class to handle all the possible shortcut keys for each state.~~
- [ ] ~~See if the canvas fill can be done once and not every frame per gamestate~~
