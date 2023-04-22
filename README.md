# ODriveConfigurator

I was tired of writing long strings to check or set parameters and not being able to have a clear view of what the parameters are set to, so I made a configurator.

Some parameters are not present as I didn't need them myself, but feel free to add them yourself and make a PR.

## Usage/Examples

`pip install -r requirements.txt`

`python ODriveConfigurator.py`



## FAQ

#### What does x parameter do?
I don't know, I just made the app to configure them, please refer to the ODrive reference.

#### Does it work with ODrive Pro or S1?
No, some of the parameters are accessed differently on the Pro and S1, and theres also alot more parameters, but you can change `params.py` to make it work if you really want to.

#### Does it work with the ODrive v3.6?
Yes!, I've tested it on my own Makerbase v3.6 clone which is running 0.5.5 firmware.

#### Your code sucks!
I know.

## Roadmap

- Ability to control update interval via UI

- Ability to switch between dark mode and light mode via UI(line 11 in ODriveConfigurator.py)

- Export and import configuration


## Screenshots

![Screenshot 2023-04-20 224416](https://user-images.githubusercontent.com/41790044/233484816-e6c8f500-6430-45c6-b94f-40c0a9828388.png)

## Authors

- [@JustAFriendlyCat](https://www.github.com/JustAFriendlyCat)
- [@disconsolated](https://github.com/disconsolated)