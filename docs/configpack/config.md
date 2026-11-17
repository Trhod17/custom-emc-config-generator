# Config Yaml Spec

```yaml
#Config Name {Required}
name: Example
#Config Pack ID {Required}
cpid: example
#Modpack Version {Optional}
modpack_version: 1.0.0
#List of Mods {Required}
mods:
    #Mod Entry
    minecraft:
        #Mod EMC file names
        configs:
            - minecraft/items
            - minecraft/blocks
            - minecraft/armor
            - minecraft/tools
        #Name {Required}
        name: Minecraft
        #Version {Optional}
        version: 1.2.5
    computercraft:
        configs:
            - computercraft
        name: ComputerCraft
        version: 1.33
printers:
    # Required Current Supported Values
    # customemc, tekkitrestrict, essentials
    - customemc
    - tekkitrestrict
    - essentials
```

# Reference

## Name (Required)

```yaml
name: Example
#Human-readable name for config pack {Required}
```

## cpid (Required)

```yaml
cpid: example
#Config Pack ID {Required}
#No Spaces or Special Characters
```

## modpack_version (Required)

```yaml
modpack_version: 1.0.0
#Set the version of the modpack
```

## mods (Required)

A listing of all the mods in the modpack

### Mod Entry
```yaml
mods:
    #Mod Entry
    minecraft:
        #Mod EMC file names without .yml extension
        configs:
            - minecraft/items
            - minecraft/blocks
            - minecraft/armor
            - minecraft/tools
        #Name {Required}
        name: Minecraft
        #Version {Optional}
        version: 1.2.5
    #...
```

## Printers
Printers create the various emc configs
