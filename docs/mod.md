# Mod Yaml Spec

---

```yaml
log:
    id: 17 #Required
    meta: 0 #Required
    emc: 32 # Must have Either an emc value or a Recipe as shown below
planks:
    id: 5
    meta: 0
    recipe:
        -   item: log
            qty: 1
    qty_from_craft: 4 # Items with a Recipe must have a qty_from_craft {Required}
```

# Item Options

## id (Required)
```yaml
id: 1 # a number
```

## meta (Required)
```yaml
meta: 1 
# The number that follows an item id after a : e.g if the item id is
#5 and the meta is 1 (5:1) you get birch planks
```

## emc (Semi - Optional)
> [!IMPORTANT]
> Items must have either an emc value or a recipe.

```yaml
emc: 0 
#Any number between 0 and 2,147,483,647 
# (EE2s Max EMC, the 32 bit integer limit)
```

## recipe (Semi - Optional)
> [!IMPORTANT]
> Items must have either an emc value or a recipe.

```yaml
recipe:
    #Up to nine entries
    #Make sure the total qty of all items dosent exceed 9
        -   item: log
            qty: 1 #number between 1-9 (how many in the crafting grid)
```

### qty_from_craft (Required)
```yaml
qty_from_craft: 1 #number between 1 - 64
```

# CustomEMC Extras (All Optional)
Some extra options that allow you to take advantage of the other functions of CustomEmc

##  AddCovRepairable (Add Convalance dust Repair Recipe)
```yaml
iron_pickaxe:
  #...
    custom_emc_extras:
        # 1 - 8 dusts for the 8 remaining slots in the crafting table
        num_dusts: 3
        # 1 - 3 corresponding to one of the three tiers of covalance dust 
        dust_tier: 1    
```

## AddAsFuel (Mark an item as fuel for EE2 items e.g Swiftwolfs Rending Gale)
```yaml
nikolite:
  #...
    custom_emc_extras:
        add_as_fuel: true # Default false
```

## AddChargedItem (Marks the specified ID as a item that can't be repaired with the Talisman of Repair)
```yaml
nikolite:
  #...
    custom_emc_extras:
        unrepairable: true # Default false
```

## AddOreBlock (Adds a the block into Equivelent Exchange's Ore block mapping for it's pickaxes)
```yaml
nikolite:
  #...
    custom_emc_extras:
        add_ore: true # Default false
```
