# EMC Config Generator

Only supports modpacks that use EE2 for minecraft 1.2.5

## Supported ways of modification
- CustomEMC (In [mods](mods/1.2.5) folder)(Simply place in modpack mods folder and copy the CustomEmc.cfg in the output directory)
- [Tekkit Restrict](https://dev.bukkit.org/projects/tekkit-restrict)

### Non-Emc Modifications
- Essentials worth.yml and items.csv

## Config Packs

Check the Github Wiki or

Info in [wiki](wiki/) folder

- [Modpack layout](wiki/layout.md)
- [modpack.yml spec](docs/home.md)
- [{mod}.yml spec](docs/mod.md)

## Requirements
- Python 3.x
- `packaging`
- `Pygments`
- `PyYAML`
- `rich`


## Usage
1. Clone the repository or Download from [releases](https://github.com/Trhod17/custom-emc-config-generator/releases) (Download `Source code (zip)`)
2. Install the required Python packages:
```bash
pip install -r requirements.txt
```
3. Create or edit modpacks in the modpacks directory
4. Run the script
```bash
python main.py
```
