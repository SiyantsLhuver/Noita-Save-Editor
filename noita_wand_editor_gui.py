from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional



SPELLS = [
    {"id": 'BOMB', "name": 'Bomb', "type": 'PROJECTILE', "mana": 25, "price": 200, "max_uses": 3},
    {"id": 'LIGHT_BULLET', "name": 'Spark bolt', "type": 'PROJECTILE', "mana": 5, "price": 100, "max_uses": None},
    {"id": 'LIGHT_BULLET_TRIGGER', "name": 'Spark bolt with trigger', "type": 'PROJECTILE', "mana": 10, "price": 140, "max_uses": None},
    {"id": 'LIGHT_BULLET_TRIGGER_2', "name": 'Spark bolt with double trigger', "type": 'PROJECTILE', "mana": 15, "price": 250, "max_uses": None},
    {"id": 'LIGHT_BULLET_TIMER', "name": 'Spark bolt with timer', "type": 'PROJECTILE', "mana": 10, "price": 140, "max_uses": None},
    {"id": 'BULLET', "name": 'Magic arrow', "type": 'PROJECTILE', "mana": 20, "price": 150, "max_uses": None},
    {"id": 'BULLET_TRIGGER', "name": 'Magic arrow with trigger', "type": 'PROJECTILE', "mana": 35, "price": 190, "max_uses": None},
    {"id": 'BULLET_TIMER', "name": 'Magic arrow with timer', "type": 'PROJECTILE', "mana": 35, "price": 190, "max_uses": None},
    {"id": 'HEAVY_BULLET', "name": 'Magic bolt', "type": 'PROJECTILE', "mana": 30, "price": 200, "max_uses": None},
    {"id": 'HEAVY_BULLET_TRIGGER', "name": 'Magic bolt with trigger', "type": 'PROJECTILE', "mana": 40, "price": 240, "max_uses": None},
    {"id": 'HEAVY_BULLET_TIMER', "name": 'Magic bolt with timer', "type": 'PROJECTILE', "mana": 40, "price": 240, "max_uses": None},
    {"id": 'AIR_BULLET', "name": 'Burst of air', "type": 'PROJECTILE', "mana": 5, "price": 80, "max_uses": None},
    {"id": 'SLOW_BULLET', "name": 'Energy orb', "type": 'PROJECTILE', "mana": 30, "price": 160, "max_uses": None},
    {"id": 'SLOW_BULLET_TRIGGER', "name": 'Energy orb with a trigger', "type": 'PROJECTILE', "mana": 50, "price": 200, "max_uses": None},
    {"id": 'SLOW_BULLET_TIMER', "name": 'Energy orb with a timer', "type": 'PROJECTILE', "mana": 50, "price": 200, "max_uses": None},
    {"id": 'BLACK_HOLE', "name": 'Black hole', "type": 'PROJECTILE', "mana": 180, "price": 200, "max_uses": 3},
    {"id": 'BLACK_HOLE_DEATH_TRIGGER', "name": 'Black Hole with Death Trigger', "type": 'PROJECTILE', "mana": 200, "price": 220, "max_uses": 3},
    {"id": 'BLACK_HOLE_BIG', "name": 'Giga black hole', "type": 'STATIC_PROJECTILE', "mana": 240, "price": 320, "max_uses": 6},
    {"id": 'BLACK_HOLE_GIGA', "name": 'Omega Black Hole', "type": 'STATIC_PROJECTILE', "mana": 500, "price": 600, "max_uses": 6},
    {"id": 'TENTACLE_PORTAL', "name": 'Eldritch portal', "type": 'PROJECTILE', "mana": 140, "price": 220, "max_uses": 5},
    {"id": 'SPITTER', "name": 'Spitter bolt', "type": 'PROJECTILE', "mana": 5, "price": 110, "max_uses": None},
    {"id": 'SPITTER_TIMER', "name": 'Spitter bolt with timer', "type": 'PROJECTILE', "mana": 10, "price": 140, "max_uses": None},
    {"id": 'SPITTER_TIER_2', "name": 'Large spitter bolt', "type": 'PROJECTILE', "mana": 25, "price": 190, "max_uses": None},
    {"id": 'SPITTER_TIER_2_TIMER', "name": 'Large spitter bolt with timer', "type": 'PROJECTILE', "mana": 30, "price": 220, "max_uses": None},
    {"id": 'SPITTER_TIER_3', "name": 'Giant spitter bolt', "type": 'PROJECTILE', "mana": 40, "price": 240, "max_uses": None},
    {"id": 'SPITTER_TIER_3_TIMER', "name": 'Giant spitter bolt with timer', "type": 'PROJECTILE', "mana": 45, "price": 260, "max_uses": None},
    {"id": 'BUBBLESHOT', "name": 'Bubble spark', "type": 'PROJECTILE', "mana": 5, "price": 100, "max_uses": None},
    {"id": 'BUBBLESHOT_TRIGGER', "name": 'Bubble spark with trigger', "type": 'PROJECTILE', "mana": 16, "price": 120, "max_uses": None},
    {"id": 'DISC_BULLET', "name": 'Disc projectile', "type": 'PROJECTILE', "mana": 20, "price": 120, "max_uses": None},
    {"id": 'DISC_BULLET_BIG', "name": 'Giga disc projectile', "type": 'PROJECTILE', "mana": 38, "price": 180, "max_uses": None},
    {"id": 'DISC_BULLET_BIGGER', "name": 'Summon Omega Sawblade', "type": 'PROJECTILE', "mana": 70, "price": 270, "max_uses": None},
    {"id": 'BOUNCY_ORB', "name": 'Energy sphere', "type": 'PROJECTILE', "mana": 20, "price": 120, "max_uses": None},
    {"id": 'BOUNCY_ORB_TIMER', "name": 'Energy sphere with timer', "type": 'PROJECTILE', "mana": 50, "price": 150, "max_uses": None},
    {"id": 'RUBBER_BALL', "name": 'Bouncing burst', "type": 'PROJECTILE', "mana": 5, "price": 60, "max_uses": None},
    {"id": 'ARROW', "name": 'Arrow', "type": 'PROJECTILE', "mana": 15, "price": 140, "max_uses": None},
    {"id": 'POLLEN', "name": 'Pollen', "type": 'PROJECTILE', "mana": 10, "price": 110, "max_uses": None},
    {"id": 'LANCE', "name": 'Glowing lance', "type": 'PROJECTILE', "mana": 30, "price": 180, "max_uses": None},
    {"id": 'ROCKET', "name": 'Magic missile', "type": 'PROJECTILE', "mana": 70, "price": 220, "max_uses": 10},
    {"id": 'ROCKET_TIER_2', "name": 'Large magic missile', "type": 'PROJECTILE', "mana": 90, "price": 240, "max_uses": 8},
    {"id": 'ROCKET_TIER_3', "name": 'Giant magic missile', "type": 'PROJECTILE', "mana": 120, "price": 250, "max_uses": 6},
    {"id": 'GRENADE', "name": 'Firebolt', "type": 'PROJECTILE', "mana": 50, "price": 170, "max_uses": 25},
    {"id": 'GRENADE_TRIGGER', "name": 'Firebolt with trigger', "type": 'PROJECTILE', "mana": 50, "price": 210, "max_uses": 25},
    {"id": 'GRENADE_TIER_2', "name": 'Large firebolt', "type": 'PROJECTILE', "mana": 90, "price": 220, "max_uses": 20},
    {"id": 'GRENADE_TIER_3', "name": 'Giant firebolt', "type": 'PROJECTILE', "mana": 90, "price": 220, "max_uses": 20},
    {"id": 'GRENADE_ANTI', "name": 'Odd Firebolt', "type": 'PROJECTILE', "mana": 50, "price": 170, "max_uses": 25},
    {"id": 'GRENADE_LARGE', "name": 'Dropper bolt', "type": 'PROJECTILE', "mana": 80, "price": 150, "max_uses": 35},
    {"id": 'MINE', "name": 'Unstable crystal', "type": 'PROJECTILE', "mana": 20, "price": 200, "max_uses": 15},
    {"id": 'MINE_DEATH_TRIGGER', "name": 'Unstable crystal with trigger', "type": 'PROJECTILE', "mana": 20, "price": 240, "max_uses": 15},
    {"id": 'PIPE_BOMB', "name": 'Dormant crystal', "type": 'PROJECTILE', "mana": 20, "price": 200, "max_uses": 20},
    {"id": 'PIPE_BOMB_DEATH_TRIGGER', "name": 'Dormant crystal with trigger', "type": 'PROJECTILE', "mana": 20, "price": 230, "max_uses": 20},
    {"id": 'EXPLODING_DEER', "name": 'Summon deercoy', "type": 'PROJECTILE', "mana": 120, "price": 170, "max_uses": 10},
    {"id": 'EXPLODING_DUCKS', "name": 'Flock of Ducks', "type": 'PROJECTILE', "mana": 100, "price": 200, "max_uses": 20},
    {"id": 'WORM_SHOT', "name": 'Worm Launcher', "type": 'PROJECTILE', "mana": 150, "price": 200, "max_uses": 10},
    {"id": 'BOMB_DETONATOR', "name": 'Explosive Detonator', "type": 'STATIC_PROJECTILE', "mana": 50, "price": 120, "max_uses": None},
    {"id": 'LASER', "name": 'Concentrated light', "type": 'PROJECTILE', "mana": 30, "price": 180, "max_uses": None},
    {"id": 'MEGALASER', "name": 'Intense concentrated light', "type": 'PROJECTILE', "mana": 110, "price": 300, "max_uses": None},
    {"id": 'LIGHTNING', "name": 'Lightning bolt', "type": 'PROJECTILE', "mana": 70, "price": 250, "max_uses": None},
    {"id": 'BALL_LIGHTNING', "name": 'Ball Lightning', "type": 'PROJECTILE', "mana": 70, "price": 250, "max_uses": None},
    {"id": 'LASER_EMITTER', "name": 'Plasma beam', "type": 'PROJECTILE', "mana": 60, "price": 180, "max_uses": None},
    {"id": 'LASER_EMITTER_FOUR', "name": 'Plasma Beam Cross', "type": 'PROJECTILE', "mana": 80, "price": 200, "max_uses": None},
    {"id": 'LASER_EMITTER_CUTTER', "name": 'Plasma Cutter', "type": 'PROJECTILE', "mana": 40, "price": 120, "max_uses": None},
    {"id": 'DIGGER', "name": 'Digging bolt', "type": 'PROJECTILE', "mana": 0, "price": 70, "max_uses": None},
    {"id": 'POWERDIGGER', "name": 'Digging blast', "type": 'PROJECTILE', "mana": 0, "price": 110, "max_uses": None},
    {"id": 'CHAINSAW', "name": 'Chainsaw', "type": 'PROJECTILE', "mana": 1, "price": 80, "max_uses": None},
    {"id": 'LUMINOUS_DRILL', "name": 'Luminous drill', "type": 'PROJECTILE', "mana": 10, "price": 150, "max_uses": None},
    {"id": 'LASER_LUMINOUS_DRILL', "name": 'Luminous drill with timer', "type": 'PROJECTILE', "mana": 30, "price": 220, "max_uses": None},
    {"id": 'TENTACLE', "name": 'Summon Tentacle', "type": 'PROJECTILE', "mana": 20, "price": 200, "max_uses": None},
    {"id": 'TENTACLE_TIMER', "name": 'Summon Tentacle with timer', "type": 'PROJECTILE', "mana": 20, "price": 250, "max_uses": None},
    {"id": 'HEAL_BULLET', "name": 'Healing bolt', "type": 'PROJECTILE', "mana": 15, "price": 60, "max_uses": 20},
    {"id": 'SPIRAL_SHOT', "name": 'Spiral shot', "type": 'PROJECTILE', "mana": 50, "price": 190, "max_uses": 15},
    {"id": 'MAGIC_SHIELD', "name": 'Magic guard', "type": 'PROJECTILE', "mana": 40, "price": 100, "max_uses": None},
    {"id": 'BIG_MAGIC_SHIELD', "name": 'Big magic guard', "type": 'PROJECTILE', "mana": 60, "price": 120, "max_uses": None},
    {"id": 'CHAIN_BOLT', "name": 'Chain bolt', "type": 'PROJECTILE', "mana": 80, "price": 240, "max_uses": None},
    {"id": 'FIREBALL', "name": 'Fireball', "type": 'PROJECTILE', "mana": 70, "price": 220, "max_uses": 15},
    {"id": 'METEOR', "name": 'Meteor', "type": 'PROJECTILE', "mana": 150, "price": 280, "max_uses": 10},
    {"id": 'FLAMETHROWER', "name": 'Flamethrower', "type": 'PROJECTILE', "mana": 20, "price": 220, "max_uses": 60},
    {"id": 'ICEBALL', "name": 'Iceball', "type": 'PROJECTILE', "mana": 90, "price": 260, "max_uses": 15},
    {"id": 'SLIMEBALL', "name": 'Slimeball', "type": 'PROJECTILE', "mana": 20, "price": 130, "max_uses": None},
    {"id": 'DARKFLAME', "name": 'Path of dark flame', "type": 'PROJECTILE', "mana": 90, "price": 180, "max_uses": 60},
    {"id": 'MISSILE', "name": 'Summon missile', "type": 'PROJECTILE', "mana": 60, "price": 200, "max_uses": 20},
    {"id": 'FUNKY_SPELL', "name": 'Funky Spell', "type": 'PROJECTILE', "mana": 5, "price": 50, "max_uses": None},
    {"id": 'PEBBLE', "name": 'Summon rock spirit', "type": 'PROJECTILE', "mana": 120, "price": 200, "max_uses": 10},
    {"id": 'DYNAMITE', "name": 'Dynamite', "type": 'PROJECTILE', "mana": 50, "price": 160, "max_uses": 16},
    {"id": 'GLITTER_BOMB', "name": 'Glitter bomb', "type": 'PROJECTILE', "mana": 70, "price": 200, "max_uses": 16},
    {"id": 'BUCKSHOT', "name": 'Triplicate bolt', "type": 'PROJECTILE', "mana": 25, "price": 160, "max_uses": None},
    {"id": 'FREEZING_GAZE', "name": 'Freezing gaze', "type": 'PROJECTILE', "mana": 45, "price": 180, "max_uses": 20},
    {"id": 'GLOWING_BOLT', "name": 'Pinpoint of light', "type": 'PROJECTILE', "mana": 65, "price": 220, "max_uses": None},
    {"id": 'SPORE_POD', "name": 'Prickly Spore Pod', "type": 'PROJECTILE', "mana": 20, "price": 200, "max_uses": None},
    {"id": 'GLUE_SHOT', "name": 'Glue Ball', "type": 'PROJECTILE', "mana": 25, "price": 140, "max_uses": None},
    {"id": 'BOMB_HOLY', "name": 'Holy Bomb', "type": 'PROJECTILE', "mana": 300, "price": 400, "max_uses": 2},
    {"id": 'BOMB_HOLY_GIGA', "name": 'Giga Holy Bomb', "type": 'PROJECTILE', "mana": 600, "price": 600, "max_uses": 2},
    {"id": 'PROPANE_TANK', "name": 'Propane tank', "type": 'PROJECTILE', "mana": 75, "price": 200, "max_uses": 10},
    {"id": 'BOMB_CART', "name": 'Bomb cart', "type": 'PROJECTILE', "mana": 75, "price": 200, "max_uses": 6},
    {"id": 'CURSED_ORB', "name": 'Cursed sphere', "type": 'PROJECTILE', "mana": 40, "price": 200, "max_uses": None},
    {"id": 'EXPANDING_ORB', "name": 'Expanding Sphere', "type": 'PROJECTILE', "mana": 70, "price": 200, "max_uses": None},
    {"id": 'CRUMBLING_EARTH', "name": 'Earthquake', "type": 'PROJECTILE', "mana": 240, "price": 300, "max_uses": 3},
    {"id": 'SUMMON_ROCK', "name": 'Rock', "type": 'PROJECTILE', "mana": 100, "price": 160, "max_uses": 3},
    {"id": 'SUMMON_EGG', "name": 'Summon egg', "type": 'PROJECTILE', "mana": 100, "price": 220, "max_uses": 2},
    {"id": 'SUMMON_HOLLOW_EGG', "name": 'Summon hollow egg', "type": 'PROJECTILE', "mana": 30, "price": 140, "max_uses": None},
    {"id": 'TNTBOX', "name": 'Summon Explosive Box', "type": 'PROJECTILE', "mana": 40, "price": 150, "max_uses": 15},
    {"id": 'TNTBOX_BIG', "name": 'Summon Large Explosive Box', "type": 'PROJECTILE', "mana": 40, "price": 170, "max_uses": 15},
    {"id": 'SWARM_FLY', "name": 'Summon fly swarm', "type": 'STATIC_PROJECTILE', "mana": 70, "price": 90, "max_uses": None},
    {"id": 'SWARM_FIREBUG', "name": 'Summon Firebug swarm', "type": 'STATIC_PROJECTILE', "mana": 80, "price": 100, "max_uses": None},
    {"id": 'SWARM_WASP', "name": 'Summon Wasp swarm', "type": 'STATIC_PROJECTILE', "mana": 90, "price": 120, "max_uses": None},
    {"id": 'FRIEND_FLY', "name": 'Summon Friendly fly', "type": 'STATIC_PROJECTILE', "mana": 120, "price": 160, "max_uses": None},
    {"id": 'ACIDSHOT', "name": 'Acid ball', "type": 'PROJECTILE', "mana": 20, "price": 180, "max_uses": 20},
    {"id": 'THUNDERBALL', "name": 'Thunder charge', "type": 'PROJECTILE', "mana": 120, "price": 300, "max_uses": 3},
    {"id": 'FIREBOMB', "name": 'Firebomb', "type": 'PROJECTILE', "mana": 10, "price": 90, "max_uses": None},
    {"id": 'SOILBALL', "name": 'Chunk of soil', "type": 'MATERIAL', "mana": 5, "price": 10, "max_uses": None},
    {"id": 'DEATH_CROSS', "name": 'Death cross', "type": 'PROJECTILE', "mana": 80, "price": 210, "max_uses": None},
    {"id": 'DEATH_CROSS_BIG', "name": 'Giga death cross', "type": 'PROJECTILE', "mana": 150, "price": 310, "max_uses": 8},
    {"id": 'INFESTATION', "name": 'Infestation', "type": 'PROJECTILE', "mana": 40, "price": 160, "max_uses": None},
    {"id": 'WALL_HORIZONTAL', "name": 'Horizontal barrier', "type": 'STATIC_PROJECTILE', "mana": 70, "price": 160, "max_uses": None},
    {"id": 'WALL_VERTICAL', "name": 'Vertical barrier', "type": 'STATIC_PROJECTILE', "mana": 70, "price": 160, "max_uses": None},
    {"id": 'WALL_SQUARE', "name": 'Square barrier', "type": 'STATIC_PROJECTILE', "mana": 70, "price": 160, "max_uses": 20},
    {"id": 'TEMPORARY_WALL', "name": 'Summon Wall', "type": 'UTILITY', "mana": 40, "price": 100, "max_uses": 20},
    {"id": 'TEMPORARY_PLATFORM', "name": 'Summon Platform', "type": 'UTILITY', "mana": 30, "price": 90, "max_uses": 20},
    {"id": 'PURPLE_EXPLOSION_FIELD', "name": 'Glittering field', "type": 'STATIC_PROJECTILE', "mana": 90, "price": 160, "max_uses": 20},
    {"id": 'DELAYED_SPELL', "name": 'Delayed spellcast', "type": 'STATIC_PROJECTILE', "mana": 20, "price": 240, "max_uses": None},
    {"id": 'LONG_DISTANCE_CAST', "name": 'Long-distance cast', "type": 'UTILITY', "mana": 0, "price": 90, "max_uses": None},
    {"id": 'TELEPORT_CAST', "name": 'Teleporting cast', "type": 'UTILITY', "mana": 100, "price": 190, "max_uses": None},
    {"id": 'SUPER_TELEPORT_CAST', "name": 'Warp cast', "type": 'UTILITY', "mana": 20, "price": 160, "max_uses": None},
    {"id": 'MIST_RADIOACTIVE', "name": 'Toxic mist', "type": 'PROJECTILE', "mana": 40, "price": 80, "max_uses": None},
    {"id": 'MIST_ALCOHOL', "name": 'mist of spirits', "type": 'PROJECTILE', "mana": 40, "price": 80, "max_uses": None},
    {"id": 'MIST_SLIME', "name": 'Slime mist', "type": 'PROJECTILE', "mana": 40, "price": 80, "max_uses": None},
    {"id": 'MIST_BLOOD', "name": 'Blood mist', "type": 'PROJECTILE', "mana": 40, "price": 120, "max_uses": 10},
    {"id": 'CIRCLE_FIRE', "name": 'Circle of fire', "type": 'MATERIAL', "mana": 20, "price": 170, "max_uses": 15},
    {"id": 'CIRCLE_ACID', "name": 'Circle of acid', "type": 'MATERIAL', "mana": 40, "price": 180, "max_uses": 4},
    {"id": 'CIRCLE_OIL', "name": 'Circle of oil', "type": 'MATERIAL', "mana": 20, "price": 160, "max_uses": 15},
    {"id": 'CIRCLE_WATER', "name": 'Circle of water', "type": 'MATERIAL', "mana": 20, "price": 160, "max_uses": 15},
    {"id": 'MATERIAL_WATER', "name": 'Water', "type": 'MATERIAL', "mana": 0, "price": 110, "max_uses": None},
    {"id": 'MATERIAL_OIL', "name": 'Oil', "type": 'MATERIAL', "mana": 0, "price": 140, "max_uses": None},
    {"id": 'MATERIAL_BLOOD', "name": 'Blood', "type": 'MATERIAL', "mana": 0, "price": 130, "max_uses": 250},
    {"id": 'MATERIAL_ACID', "name": 'Acid', "type": 'MATERIAL', "mana": 0, "price": 150, "max_uses": None},
    {"id": 'MATERIAL_CEMENT', "name": 'Cement', "type": 'MATERIAL', "mana": 0, "price": 100, "max_uses": None},
    {"id": 'TELEPORT_PROJECTILE', "name": 'Teleport bolt', "type": 'PROJECTILE', "mana": 40, "price": 130, "max_uses": None},
    {"id": 'TELEPORT_PROJECTILE_SHORT', "name": 'Small Teleport Bolt', "type": 'PROJECTILE', "mana": 20, "price": 130, "max_uses": None},
    {"id": 'TELEPORT_PROJECTILE_STATIC', "name": 'Return', "type": 'PROJECTILE', "mana": 40, "price": 90, "max_uses": None},
    {"id": 'SWAPPER_PROJECTILE', "name": 'Swapper', "type": 'PROJECTILE', "mana": 5, "price": 100, "max_uses": None},
    {"id": 'TELEPORT_PROJECTILE_CLOSER', "name": 'Homebringer Teleport Bolt', "type": 'PROJECTILE', "mana": 20, "price": 130, "max_uses": None},
    {"id": 'NUKE', "name": 'Nuke', "type": 'PROJECTILE', "mana": 200, "price": 400, "max_uses": 1},
    {"id": 'NUKE_GIGA', "name": 'Giga Nuke', "type": 'PROJECTILE', "mana": 500, "price": 800, "max_uses": 1},
    {"id": 'FIREWORK', "name": 'Fireworks!', "type": 'PROJECTILE', "mana": 70, "price": 220, "max_uses": 25},
    {"id": 'TOUCH_GOLD', "name": 'Touch of Gold', "type": 'MATERIAL', "mana": 300, "price": 480, "max_uses": 1},
    {"id": 'TOUCH_WATER', "name": 'Touch of Water', "type": 'MATERIAL', "mana": 280, "price": 420, "max_uses": 5},
    {"id": 'TOUCH_OIL', "name": 'Touch of Oil', "type": 'MATERIAL', "mana": 260, "price": 380, "max_uses": 5},
    {"id": 'TOUCH_ALCOHOL', "name": 'Touch of Spirits', "type": 'MATERIAL', "mana": 240, "price": 360, "max_uses": 5},
    {"id": 'TOUCH_BLOOD', "name": 'Touch of Blood', "type": 'MATERIAL', "mana": 270, "price": 390, "max_uses": 3},
    {"id": 'TOUCH_SMOKE', "name": 'Touch of Smoke', "type": 'MATERIAL', "mana": 230, "price": 350, "max_uses": 5},
    {"id": 'DESTRUCTION', "name": 'Destruction', "type": 'STATIC_PROJECTILE', "mana": 600, "price": 600, "max_uses": 5},
    {"id": 'BURST_2', "name": 'Double spell', "type": 'DRAW_MANY', "mana": 0, "price": 140, "max_uses": None},
    {"id": 'BURST_3', "name": 'Triple spell', "type": 'DRAW_MANY', "mana": 2, "price": 160, "max_uses": None},
    {"id": 'BURST_4', "name": 'Quadruple spell', "type": 'DRAW_MANY', "mana": 5, "price": 180, "max_uses": None},
    {"id": 'BURST_8', "name": 'Octuple spell', "type": 'DRAW_MANY', "mana": 30, "price": 300, "max_uses": None},
    {"id": 'BURST_X', "name": 'Myriad Spell', "type": 'DRAW_MANY', "mana": 50, "price": 500, "max_uses": 30},
    {"id": 'SCATTER_3', "name": 'Triple scatter spell', "type": 'DRAW_MANY', "mana": 1, "price": 120, "max_uses": None},
    {"id": 'SCATTER_4', "name": 'Quadruple scatter spell', "type": 'DRAW_MANY', "mana": 2, "price": 140, "max_uses": None},
    {"id": 'I_SHAPE', "name": 'Formation - behind your back', "type": 'DRAW_MANY', "mana": 0, "price": 80, "max_uses": None},
    {"id": 'Y_SHAPE', "name": 'Formation - bifurcated', "type": 'DRAW_MANY', "mana": 2, "price": 100, "max_uses": None},
    {"id": 'T_SHAPE', "name": 'Formation - above and below', "type": 'DRAW_MANY', "mana": 3, "price": 120, "max_uses": None},
    {"id": 'W_SHAPE', "name": 'Formation - trifurcated', "type": 'DRAW_MANY', "mana": 3, "price": 160, "max_uses": None},
    {"id": 'CIRCLE_SHAPE', "name": 'Formation - hexagon', "type": 'DRAW_MANY', "mana": 6, "price": 150, "max_uses": None},
    {"id": 'PENTAGRAM_SHAPE', "name": 'Formation - pentagon', "type": 'DRAW_MANY', "mana": 5, "price": 150, "max_uses": None},
    {"id": 'SPREAD_REDUCE', "name": 'Reduce spread', "type": 'MODIFIER', "mana": 1, "price": 100, "max_uses": None},
    {"id": 'HEAVY_SPREAD', "name": 'Heavy spread', "type": 'MODIFIER', "mana": 2, "price": 100, "max_uses": None},
    {"id": 'RECHARGE', "name": 'Reduce recharge time', "type": 'MODIFIER', "mana": 12, "price": 200, "max_uses": None},
    {"id": 'LIFETIME', "name": 'Increase lifetime', "type": 'MODIFIER', "mana": 40, "price": 250, "max_uses": None},
    {"id": 'LIFETIME_DOWN', "name": 'Reduce lifetime', "type": 'MODIFIER', "mana": 10, "price": 90, "max_uses": None},
    {"id": 'NOLLA', "name": 'Nolla', "type": 'MODIFIER', "mana": 1, "price": 50, "max_uses": None},
    {"id": 'SLOW_BUT_STEADY', "name": 'Slow But Steady', "type": 'MODIFIER', "mana": 0, "price": 50, "max_uses": None},
    {"id": 'EXPLOSION_REMOVE', "name": 'Remove Explosion', "type": 'MODIFIER', "mana": 0, "price": 50, "max_uses": None},
    {"id": 'EXPLOSION_TINY', "name": 'Concentrated Explosion', "type": 'MODIFIER', "mana": 40, "price": 160, "max_uses": None},
    {"id": 'LASER_EMITTER_WIDER', "name": 'Plasma Beam Enhancer', "type": 'MODIFIER', "mana": 10, "price": 40, "max_uses": None},
    {"id": 'MANA_REDUCE', "name": 'Add mana', "type": 'MODIFIER', "mana": -30, "price": 250, "max_uses": None},
    {"id": 'BLOOD_MAGIC', "name": 'Blood magic', "type": 'UTILITY', "mana": -100, "price": 150, "max_uses": None},
    {"id": 'MONEY_MAGIC', "name": 'Gold to Power', "type": 'UTILITY', "mana": 30, "price": 200, "max_uses": None},
    {"id": 'BLOOD_TO_POWER', "name": 'Blood to Power', "type": 'UTILITY', "mana": 20, "price": 150, "max_uses": None},
    {"id": 'DUPLICATE', "name": 'Spell duplication', "type": 'OTHER', "mana": 250, "price": 250, "max_uses": None},
    {"id": 'QUANTUM_SPLIT', "name": 'Quantum Split', "type": 'MODIFIER', "mana": 10, "price": 200, "max_uses": None},
    {"id": 'GRAVITY', "name": 'Gravity', "type": 'MODIFIER', "mana": 1, "price": 50, "max_uses": None},
    {"id": 'GRAVITY_ANTI', "name": 'Anti-gravity', "type": 'MODIFIER', "mana": 1, "price": 50, "max_uses": None},
    {"id": 'SINEWAVE', "name": 'Slithering path', "type": 'MODIFIER', "mana": 0, "price": 10, "max_uses": None},
    {"id": 'CHAOTIC_ARC', "name": 'Chaotic path', "type": 'MODIFIER', "mana": 0, "price": 10, "max_uses": None},
    {"id": 'PINGPONG_PATH', "name": 'Ping-pong path', "type": 'MODIFIER', "mana": 0, "price": 20, "max_uses": None},
    {"id": 'AVOIDING_ARC', "name": 'Avoiding arc', "type": 'MODIFIER', "mana": 0, "price": 30, "max_uses": None},
    {"id": 'FLOATING_ARC', "name": 'Floating arc', "type": 'MODIFIER', "mana": 0, "price": 30, "max_uses": None},
    {"id": 'FLY_DOWNWARDS', "name": 'Fly downwards', "type": 'MODIFIER', "mana": 0, "price": 30, "max_uses": None},
    {"id": 'FLY_UPWARDS', "name": 'Fly upwards', "type": 'MODIFIER', "mana": 0, "price": 20, "max_uses": None},
    {"id": 'HORIZONTAL_ARC', "name": 'Horizontal path', "type": 'MODIFIER', "mana": 0, "price": 20, "max_uses": None},
    {"id": 'LINE_ARC', "name": 'Linear arc', "type": 'MODIFIER', "mana": 0, "price": 30, "max_uses": None},
    {"id": 'ORBIT_SHOT', "name": 'Orbiting Arc', "type": 'MODIFIER', "mana": 0, "price": 30, "max_uses": None},
    {"id": 'SPIRALING_SHOT', "name": 'Spiral Arc', "type": 'MODIFIER', "mana": 0, "price": 30, "max_uses": None},
    {"id": 'PHASING_ARC', "name": 'Phasing Arc', "type": 'MODIFIER', "mana": 2, "price": 170, "max_uses": None},
    {"id": 'BOUNCE', "name": 'Bounce', "type": 'MODIFIER', "mana": 0, "price": 50, "max_uses": None},
    {"id": 'REMOVE_BOUNCE', "name": 'Remove Bounce', "type": 'MODIFIER', "mana": 0, "price": 50, "max_uses": None},
    {"id": 'HOMING', "name": 'Homing', "type": 'MODIFIER', "mana": 70, "price": 220, "max_uses": None},
    {"id": 'HOMING_SHORT', "name": 'Short-range Homing', "type": 'MODIFIER', "mana": 40, "price": 160, "max_uses": None},
    {"id": 'HOMING_ROTATE', "name": 'Rotate towards foes', "type": 'MODIFIER', "mana": 40, "price": 175, "max_uses": None},
    {"id": 'HOMING_SHOOTER', "name": 'Boomerang', "type": 'MODIFIER', "mana": 10, "price": 100, "max_uses": None},
    {"id": 'AUTOAIM', "name": 'Auto-Aim', "type": 'MODIFIER', "mana": 25, "price": 150, "max_uses": None},
    {"id": 'HOMING_ACCELERATING', "name": 'Accelerative Homing', "type": 'MODIFIER', "mana": 60, "price": 180, "max_uses": None},
    {"id": 'HOMING_CURSOR', "name": 'Aiming Arc', "type": 'MODIFIER', "mana": 30, "price": 175, "max_uses": None},
    {"id": 'HOMING_AREA', "name": 'Projectile Area Teleport', "type": 'MODIFIER', "mana": 60, "price": 175, "max_uses": None},
    {"id": 'PIERCING_SHOT', "name": 'Piercing shot', "type": 'MODIFIER', "mana": 140, "price": 190, "max_uses": None},
    {"id": 'CLIPPING_SHOT', "name": 'Drilling shot', "type": 'MODIFIER', "mana": 160, "price": 200, "max_uses": None},
    {"id": 'DAMAGE', "name": 'Damage Plus', "type": 'MODIFIER', "mana": 5, "price": 140, "max_uses": None},
    {"id": 'DAMAGE_RANDOM', "name": 'Random damage', "type": 'MODIFIER', "mana": 15, "price": 200, "max_uses": None},
    {"id": 'BLOODLUST', "name": 'Bloodlust', "type": 'MODIFIER', "mana": 2, "price": 160, "max_uses": None},
    {"id": 'DAMAGE_FOREVER', "name": 'Mana To Damage', "type": 'MODIFIER', "mana": 0, "price": 240, "max_uses": 20},
    {"id": 'CRITICAL_HIT', "name": 'Critical Plus', "type": 'MODIFIER', "mana": 5, "price": 140, "max_uses": None},
    {"id": 'AREA_DAMAGE', "name": 'Damage field', "type": 'MODIFIER', "mana": 30, "price": 140, "max_uses": None},
    {"id": 'SPELLS_TO_POWER', "name": 'Spells to Power', "type": 'MODIFIER', "mana": 110, "price": 140, "max_uses": None},
    {"id": 'ESSENCE_TO_POWER', "name": 'Essence to Power', "type": 'MODIFIER', "mana": 110, "price": 120, "max_uses": None},
    {"id": 'HEAVY_SHOT', "name": 'Heavy Shot', "type": 'MODIFIER', "mana": 7, "price": 150, "max_uses": None},
    {"id": 'LIGHT_SHOT', "name": 'Light shot', "type": 'MODIFIER', "mana": 5, "price": 60, "max_uses": None},
    {"id": 'KNOCKBACK', "name": 'Knockback', "type": 'MODIFIER', "mana": 5, "price": 100, "max_uses": None},
    {"id": 'RECOIL', "name": 'Recoil', "type": 'MODIFIER', "mana": 5, "price": 100, "max_uses": None},
    {"id": 'RECOIL_DAMPER', "name": 'Recoil Damper', "type": 'MODIFIER', "mana": 5, "price": 100, "max_uses": None},
    {"id": 'SPEED', "name": 'Speed Up', "type": 'MODIFIER', "mana": 3, "price": 100, "max_uses": None},
    {"id": 'ACCELERATING_SHOT', "name": 'Accelerating shot', "type": 'MODIFIER', "mana": 20, "price": 190, "max_uses": None},
    {"id": 'DECELERATING_SHOT', "name": 'Decelerating shot', "type": 'MODIFIER', "mana": 10, "price": 80, "max_uses": None},
    {"id": 'EXPLOSIVE_PROJECTILE', "name": 'Explosive projectile', "type": 'MODIFIER', "mana": 30, "price": 120, "max_uses": None},
    {"id": 'WATER_TO_POISON', "name": 'Water to poison', "type": 'MODIFIER', "mana": 30, "price": 80, "max_uses": None},
    {"id": 'BLOOD_TO_ACID', "name": 'Blood to acid', "type": 'MODIFIER', "mana": 30, "price": 80, "max_uses": None},
    {"id": 'LAVA_TO_BLOOD', "name": 'Lava to blood', "type": 'MODIFIER', "mana": 30, "price": 80, "max_uses": None},
    {"id": 'LIQUID_TO_EXPLOSION', "name": 'Liquid Detonation', "type": 'MODIFIER', "mana": 40, "price": 120, "max_uses": None},
    {"id": 'TOXIC_TO_ACID', "name": 'Toxic sludge to acid', "type": 'MODIFIER', "mana": 50, "price": 120, "max_uses": None},
    {"id": 'STATIC_TO_SAND', "name": 'Ground to sand', "type": 'MODIFIER', "mana": 70, "price": 140, "max_uses": 8},
    {"id": 'TRANSMUTATION', "name": 'Chaotic transmutation', "type": 'MODIFIER', "mana": 80, "price": 180, "max_uses": 8},
    {"id": 'RANDOM_EXPLOSION', "name": 'Chaos magic', "type": 'MODIFIER', "mana": 120, "price": 240, "max_uses": 30},
    {"id": 'NECROMANCY', "name": 'Necromancy', "type": 'MODIFIER', "mana": 20, "price": 80, "max_uses": None},
    {"id": 'LIGHT', "name": 'Light', "type": 'MODIFIER', "mana": 1, "price": 20, "max_uses": None},
    {"id": 'EXPLOSION', "name": 'Explosion', "type": 'STATIC_PROJECTILE', "mana": 80, "price": 160, "max_uses": None},
    {"id": 'EXPLOSION_LIGHT', "name": 'Magical Explosion', "type": 'STATIC_PROJECTILE', "mana": 80, "price": 160, "max_uses": None},
    {"id": 'FIRE_BLAST', "name": 'Explosion of brimstone', "type": 'STATIC_PROJECTILE', "mana": 10, "price": 120, "max_uses": None},
    {"id": 'POISON_BLAST', "name": 'Explosion of poison', "type": 'STATIC_PROJECTILE', "mana": 30, "price": 140, "max_uses": None},
    {"id": 'ALCOHOL_BLAST', "name": 'Explosion of spirits', "type": 'STATIC_PROJECTILE', "mana": 30, "price": 140, "max_uses": None},
    {"id": 'THUNDER_BLAST', "name": 'Explosion of thunder', "type": 'STATIC_PROJECTILE', "mana": 110, "price": 180, "max_uses": None},
    {"id": 'BERSERK_FIELD', "name": 'Circle of fervour', "type": 'STATIC_PROJECTILE', "mana": 30, "price": 200, "max_uses": 15},
    {"id": 'POLYMORPH_FIELD', "name": 'Circle of transmogrification', "type": 'STATIC_PROJECTILE', "mana": 50, "price": 200, "max_uses": 5},
    {"id": 'CHAOS_POLYMORPH_FIELD', "name": 'Circle of unstable metamorphosis', "type": 'STATIC_PROJECTILE', "mana": 20, "price": 200, "max_uses": 10},
    {"id": 'ELECTROCUTION_FIELD', "name": 'Circle of thunder', "type": 'STATIC_PROJECTILE', "mana": 60, "price": 200, "max_uses": 15},
    {"id": 'FREEZE_FIELD', "name": 'Circle of stillness', "type": 'STATIC_PROJECTILE', "mana": 50, "price": 200, "max_uses": 15},
    {"id": 'REGENERATION_FIELD', "name": 'Circle of vigour', "type": 'STATIC_PROJECTILE', "mana": 80, "price": 250, "max_uses": 2},
    {"id": 'TELEPORTATION_FIELD', "name": 'Circle of displacement', "type": 'STATIC_PROJECTILE', "mana": 30, "price": 150, "max_uses": 15},
    {"id": 'LEVITATION_FIELD', "name": 'Circle of buoyancy', "type": 'STATIC_PROJECTILE', "mana": 10, "price": 120, "max_uses": 15},
    {"id": 'SHIELD_FIELD', "name": 'Circle of shielding', "type": 'STATIC_PROJECTILE', "mana": 20, "price": 160, "max_uses": 10},
    {"id": 'PROJECTILE_TRANSMUTATION_FIELD', "name": 'Projectile transmutation field', "type": 'STATIC_PROJECTILE', "mana": 120, "price": 250, "max_uses": 6},
    {"id": 'PROJECTILE_THUNDER_FIELD', "name": 'Projectile thunder field', "type": 'STATIC_PROJECTILE', "mana": 140, "price": 300, "max_uses": 6},
    {"id": 'PROJECTILE_GRAVITY_FIELD', "name": 'Projectile gravity field', "type": 'STATIC_PROJECTILE', "mana": 120, "price": 250, "max_uses": 6},
    {"id": 'VACUUM_POWDER', "name": 'Powder Vacuum Field', "type": 'STATIC_PROJECTILE', "mana": 40, "price": 150, "max_uses": 20},
    {"id": 'VACUUM_LIQUID', "name": 'Liquid Vacuum Field', "type": 'STATIC_PROJECTILE', "mana": 40, "price": 150, "max_uses": 20},
    {"id": 'VACUUM_ENTITIES', "name": 'Vacuum Field', "type": 'STATIC_PROJECTILE', "mana": 50, "price": 200, "max_uses": 20},
    {"id": 'SEA_LAVA', "name": 'Sea of lava', "type": 'MATERIAL', "mana": 140, "price": 350, "max_uses": 3},
    {"id": 'SEA_ALCOHOL', "name": 'Sea of alcohol', "type": 'MATERIAL', "mana": 140, "price": 350, "max_uses": 3},
    {"id": 'SEA_OIL', "name": 'Sea of oil', "type": 'MATERIAL', "mana": 140, "price": 350, "max_uses": 3},
    {"id": 'SEA_WATER', "name": 'Sea of water', "type": 'MATERIAL', "mana": 140, "price": 350, "max_uses": 3},
    {"id": 'SEA_ACID', "name": 'Sea of acid', "type": 'MATERIAL', "mana": 140, "price": 350, "max_uses": 3},
    {"id": 'SEA_ACID_GAS', "name": 'Sea of flammable gas', "type": 'MATERIAL', "mana": 140, "price": 200, "max_uses": 3},
    {"id": 'CLOUD_WATER', "name": 'Rain cloud', "type": 'STATIC_PROJECTILE', "mana": 30, "price": 140, "max_uses": 10},
    {"id": 'CLOUD_OIL', "name": 'Oil cloud', "type": 'STATIC_PROJECTILE', "mana": 20, "price": 100, "max_uses": 15},
    {"id": 'CLOUD_BLOOD', "name": 'Blood cloud', "type": 'STATIC_PROJECTILE', "mana": 60, "price": 200, "max_uses": 3},
    {"id": 'CLOUD_ACID', "name": 'Acid cloud', "type": 'STATIC_PROJECTILE', "mana": 90, "price": 180, "max_uses": 8},
    {"id": 'CLOUD_THUNDER', "name": 'Thundercloud', "type": 'STATIC_PROJECTILE', "mana": 90, "price": 190, "max_uses": 5},
    {"id": 'ELECTRIC_CHARGE', "name": 'Electric charge', "type": 'MODIFIER', "mana": 8, "price": 150, "max_uses": None},
    {"id": 'MATTER_EATER', "name": 'Matter eater', "type": 'MODIFIER', "mana": 120, "price": 280, "max_uses": 10},
    {"id": 'FREEZE', "name": 'Freeze charge', "type": 'MODIFIER', "mana": 10, "price": 140, "max_uses": None},
    {"id": 'HITFX_BURNING_CRITICAL_HIT', "name": 'Critical on burning', "type": 'MODIFIER', "mana": 10, "price": 70, "max_uses": None},
    {"id": 'HITFX_CRITICAL_WATER', "name": 'Critical on wet (water) enemies', "type": 'MODIFIER', "mana": 10, "price": 70, "max_uses": None},
    {"id": 'HITFX_CRITICAL_OIL', "name": 'Critical on oiled enemies', "type": 'MODIFIER', "mana": 10, "price": 70, "max_uses": None},
    {"id": 'HITFX_CRITICAL_BLOOD', "name": 'Critical on bloody enemies', "type": 'MODIFIER', "mana": 10, "price": 70, "max_uses": None},
    {"id": 'HITFX_TOXIC_CHARM', "name": 'Charm on toxic sludge', "type": 'MODIFIER', "mana": 70, "price": 150, "max_uses": None},
    {"id": 'HITFX_EXPLOSION_SLIME', "name": 'Explosion on slimy enemies', "type": 'MODIFIER', "mana": 20, "price": 140, "max_uses": None},
    {"id": 'HITFX_EXPLOSION_SLIME_GIGA', "name": 'Giant explosion on slimy enemies', "type": 'MODIFIER', "mana": 200, "price": 300, "max_uses": 20},
    {"id": 'HITFX_EXPLOSION_ALCOHOL', "name": 'Explosion on drunk enemies', "type": 'MODIFIER', "mana": 20, "price": 140, "max_uses": None},
    {"id": 'HITFX_EXPLOSION_ALCOHOL_GIGA', "name": 'Giant explosion on drunk enemies', "type": 'MODIFIER', "mana": 200, "price": 300, "max_uses": 20},
    {"id": 'HITFX_PETRIFY', "name": 'Petrify', "type": 'MODIFIER', "mana": 10, "price": 140, "max_uses": None},
    {"id": 'ROCKET_DOWNWARDS', "name": 'Downwards bolt bundle', "type": 'MODIFIER', "mana": 90, "price": 200, "max_uses": None},
    {"id": 'ROCKET_OCTAGON', "name": 'Octagonal bolt bundle', "type": 'MODIFIER', "mana": 100, "price": 200, "max_uses": None},
    {"id": 'FIZZLE', "name": 'Fizzle', "type": 'MODIFIER', "mana": 0, "price": 0, "max_uses": None},
    {"id": 'BOUNCE_EXPLOSION', "name": 'Explosive bounce', "type": 'MODIFIER', "mana": 20, "price": 180, "max_uses": None},
    {"id": 'BOUNCE_SPARK', "name": 'Bubbly bounce', "type": 'MODIFIER', "mana": 20, "price": 120, "max_uses": None},
    {"id": 'BOUNCE_LASER', "name": 'Concentrated light bounce', "type": 'MODIFIER', "mana": 30, "price": 180, "max_uses": None},
    {"id": 'BOUNCE_LASER_EMITTER', "name": 'Plasma Beam Bounce', "type": 'MODIFIER', "mana": 40, "price": 180, "max_uses": None},
    {"id": 'BOUNCE_LARPA', "name": 'Larpa Bounce', "type": 'MODIFIER', "mana": 80, "price": 250, "max_uses": None},
    {"id": 'FIREBALL_RAY', "name": 'Fireball thrower', "type": 'MODIFIER', "mana": 110, "price": 150, "max_uses": 16},
    {"id": 'LIGHTNING_RAY', "name": 'Lightning thrower', "type": 'MODIFIER', "mana": 110, "price": 180, "max_uses": 16},
    {"id": 'TENTACLE_RAY', "name": 'Tentacler', "type": 'MODIFIER', "mana": 110, "price": 150, "max_uses": 16},
    {"id": 'LASER_EMITTER_RAY', "name": 'Plasma Beam Thrower', "type": 'MODIFIER', "mana": 110, "price": 150, "max_uses": 16},
    {"id": 'FIREBALL_RAY_LINE', "name": 'Two-way fireball thrower', "type": 'MODIFIER', "mana": 130, "price": 120, "max_uses": 20},
    {"id": 'FIREBALL_RAY_ENEMY', "name": 'Personal fireball thrower', "type": 'MODIFIER', "mana": 90, "price": 100, "max_uses": 20},
    {"id": 'LIGHTNING_RAY_ENEMY', "name": 'Personal lightning caster', "type": 'MODIFIER', "mana": 90, "price": 150, "max_uses": 20},
    {"id": 'TENTACLE_RAY_ENEMY', "name": 'Personal tentacler', "type": 'MODIFIER', "mana": 90, "price": 150, "max_uses": 20},
    {"id": 'GRAVITY_FIELD_ENEMY', "name": 'Personal gravity field', "type": 'MODIFIER', "mana": 110, "price": 250, "max_uses": 20},
    {"id": 'CURSE', "name": 'Venomous Curse', "type": 'MODIFIER', "mana": 30, "price": 140, "max_uses": None},
    {"id": 'CURSE_WITHER_PROJECTILE', "name": 'Weakening Curse - Projectiles', "type": 'MODIFIER', "mana": 50, "price": 100, "max_uses": None},
    {"id": 'CURSE_WITHER_EXPLOSION', "name": 'Weakening Curse - Explosives', "type": 'MODIFIER', "mana": 50, "price": 100, "max_uses": None},
    {"id": 'CURSE_WITHER_MELEE', "name": 'Weakening Curse - Melee', "type": 'MODIFIER', "mana": 50, "price": 100, "max_uses": None},
    {"id": 'CURSE_WITHER_ELECTRICITY', "name": 'Weakening Curse - Electricity', "type": 'MODIFIER', "mana": 50, "price": 100, "max_uses": None},
    {"id": 'ORBIT_DISCS', "name": 'Sawblade Orbit', "type": 'MODIFIER', "mana": 70, "price": 200, "max_uses": None},
    {"id": 'ORBIT_FIREBALLS', "name": 'Fireball Orbit', "type": 'MODIFIER', "mana": 40, "price": 140, "max_uses": None},
    {"id": 'ORBIT_NUKES', "name": 'Nuke Orbit', "type": 'MODIFIER', "mana": 250, "price": 400, "max_uses": 3},
    {"id": 'ORBIT_LASERS', "name": 'Plasma Beam Orbit', "type": 'MODIFIER', "mana": 100, "price": 200, "max_uses": None},
    {"id": 'ORBIT_LARPA', "name": 'Orbit Larpa', "type": 'MODIFIER', "mana": 90, "price": 240, "max_uses": None},
    {"id": 'CHAIN_SHOT', "name": 'Chain Spell', "type": 'MODIFIER', "mana": 70, "price": 240, "max_uses": None},
    {"id": 'ARC_ELECTRIC', "name": 'Electric Arc', "type": 'MODIFIER', "mana": 15, "price": 170, "max_uses": None},
    {"id": 'ARC_FIRE', "name": 'Fire Arc', "type": 'MODIFIER', "mana": 15, "price": 160, "max_uses": None},
    {"id": 'ARC_GUNPOWDER', "name": 'Gunpowder Arc', "type": 'MODIFIER', "mana": 15, "price": 160, "max_uses": None},
    {"id": 'ARC_POISON', "name": 'Poison Arc', "type": 'MODIFIER', "mana": 15, "price": 160, "max_uses": None},
    {"id": 'CRUMBLING_EARTH_PROJECTILE', "name": 'Earthquake shot', "type": 'MODIFIER', "mana": 45, "price": 200, "max_uses": 15},
    {"id": 'X_RAY', "name": 'All-seeing eye', "type": 'UTILITY', "mana": 100, "price": 230, "max_uses": 10},
    {"id": 'UNSTABLE_GUNPOWDER', "name": 'Firecrackers', "type": 'MODIFIER', "mana": 15, "price": 140, "max_uses": None},
    {"id": 'ACID_TRAIL', "name": 'Acid trail', "type": 'MODIFIER', "mana": 15, "price": 160, "max_uses": None},
    {"id": 'POISON_TRAIL', "name": 'Poison trail', "type": 'MODIFIER', "mana": 10, "price": 160, "max_uses": None},
    {"id": 'OIL_TRAIL', "name": 'Oil trail', "type": 'MODIFIER', "mana": 10, "price": 160, "max_uses": None},
    {"id": 'WATER_TRAIL', "name": 'Water trail', "type": 'MODIFIER', "mana": 10, "price": 160, "max_uses": None},
    {"id": 'GUNPOWDER_TRAIL', "name": 'Gunpowder trail', "type": 'MODIFIER', "mana": 10, "price": 160, "max_uses": None},
    {"id": 'FIRE_TRAIL', "name": 'Fire trail', "type": 'MODIFIER', "mana": 10, "price": 130, "max_uses": None},
    {"id": 'BURN_TRAIL', "name": 'Burning trail', "type": 'MODIFIER', "mana": 5, "price": 100, "max_uses": None},
    {"id": 'TORCH', "name": 'Torch', "type": 'PASSIVE', "mana": 0, "price": 100, "max_uses": None},
    {"id": 'TORCH_ELECTRIC', "name": 'Electric Torch', "type": 'PASSIVE', "mana": 0, "price": 150, "max_uses": None},
    {"id": 'ENERGY_SHIELD', "name": 'Energy shield', "type": 'PASSIVE', "mana": 0, "price": 220, "max_uses": None},
    {"id": 'ENERGY_SHIELD_SECTOR', "name": 'Energy shield sector', "type": 'PASSIVE', "mana": 0, "price": 160, "max_uses": None},
    {"id": 'ENERGY_SHIELD_SHOT', "name": 'Projectile energy shield', "type": 'MODIFIER', "mana": 5, "price": 180, "max_uses": None},
    {"id": 'TINY_GHOST', "name": 'Summon Tiny Ghost', "type": 'PASSIVE', "mana": 0, "price": 160, "max_uses": None},
    {"id": 'OCARINA_A', "name": 'Ocarina - note A', "type": 'OTHER', "mana": 1, "price": 10, "max_uses": None},
    {"id": 'OCARINA_B', "name": 'Ocarina - note B', "type": 'OTHER', "mana": 1, "price": 10, "max_uses": None},
    {"id": 'OCARINA_C', "name": 'Ocarina - note C', "type": 'OTHER', "mana": 1, "price": 10, "max_uses": None},
    {"id": 'OCARINA_D', "name": 'Ocarina - note D', "type": 'OTHER', "mana": 1, "price": 10, "max_uses": None},
    {"id": 'OCARINA_E', "name": 'Ocarina - note E', "type": 'OTHER', "mana": 1, "price": 10, "max_uses": None},
    {"id": 'OCARINA_F', "name": 'Ocarina - note F', "type": 'OTHER', "mana": 1, "price": 10, "max_uses": None},
    {"id": 'OCARINA_GSHARP', "name": 'Ocarina - note G#', "type": 'OTHER', "mana": 1, "price": 10, "max_uses": None},
    {"id": 'OCARINA_A2', "name": 'Ocarina - note A2', "type": 'OTHER', "mana": 1, "price": 10, "max_uses": None},
    {"id": 'KANTELE_A', "name": 'Kantele - note A', "type": 'OTHER', "mana": 1, "price": 10, "max_uses": None},
    {"id": 'KANTELE_D', "name": 'Kantele - note D', "type": 'OTHER', "mana": 1, "price": 10, "max_uses": None},
    {"id": 'KANTELE_DIS', "name": 'Kantele - note D#', "type": 'OTHER', "mana": 1, "price": 10, "max_uses": None},
    {"id": 'KANTELE_E', "name": 'Kantele - note E', "type": 'OTHER', "mana": 1, "price": 10, "max_uses": None},
    {"id": 'KANTELE_G', "name": 'Kantele - note G', "type": 'OTHER', "mana": 1, "price": 10, "max_uses": None},
    {"id": 'RANDOM_SPELL', "name": 'Random spell', "type": 'OTHER', "mana": 5, "price": 100, "max_uses": None},
    {"id": 'RANDOM_PROJECTILE', "name": 'Random projectile spell', "type": 'PROJECTILE', "mana": 20, "price": 150, "max_uses": None},
    {"id": 'RANDOM_MODIFIER', "name": 'Random modifier spell', "type": 'MODIFIER', "mana": 20, "price": 120, "max_uses": None},
    {"id": 'RANDOM_STATIC_PROJECTILE', "name": 'Random static projectile spell', "type": 'STATIC_PROJECTILE', "mana": 20, "price": 160, "max_uses": None},
    {"id": 'DRAW_RANDOM', "name": 'Copy random spell', "type": 'OTHER', "mana": 20, "price": 150, "max_uses": None},
    {"id": 'DRAW_RANDOM_X3', "name": 'Copy random spell thrice', "type": 'OTHER', "mana": 50, "price": 250, "max_uses": None},
    {"id": 'DRAW_3_RANDOM', "name": 'Copy three random spells', "type": 'OTHER', "mana": 40, "price": 200, "max_uses": None},
    {"id": 'ALL_NUKES', "name": 'Spells to nukes', "type": 'UTILITY', "mana": 600, "price": 600, "max_uses": 2},
    {"id": 'ALL_DISCS', "name": 'Spells to giga sawblades', "type": 'UTILITY', "mana": 100, "price": 400, "max_uses": None},
    {"id": 'ALL_ROCKETS', "name": 'Spells to magic missiles', "type": 'UTILITY', "mana": 100, "price": 400, "max_uses": 10},
    {"id": 'ALL_DEATHCROSSES', "name": 'Spells to death crosses', "type": 'UTILITY', "mana": 80, "price": 350, "max_uses": 15},
    {"id": 'ALL_BLACKHOLES', "name": 'Spells to black holes', "type": 'UTILITY', "mana": 200, "price": 500, "max_uses": 10},
    {"id": 'ALL_ACID', "name": 'Spells to acid', "type": 'UTILITY', "mana": 200, "price": 600, "max_uses": None},
    {"id": 'ALL_SPELLS', "name": 'The end of everything', "type": 'OTHER', "mana": 600, "price": 1000, "max_uses": 1},
    {"id": 'SUMMON_PORTAL', "name": 'Summon portal', "type": 'OTHER', "mana": 50, "price": 100, "max_uses": 7},
    {"id": 'ADD_TRIGGER', "name": 'Add trigger', "type": 'OTHER', "mana": 10, "price": 100, "max_uses": None},
    {"id": 'ADD_TIMER', "name": 'Add timer', "type": 'OTHER', "mana": 20, "price": 150, "max_uses": None},
    {"id": 'ADD_DEATH_TRIGGER', "name": 'Add expiration trigger', "type": 'OTHER', "mana": 20, "price": 150, "max_uses": None},
    {"id": 'LARPA_CHAOS', "name": 'Chaos larpa', "type": 'MODIFIER', "mana": 100, "price": 260, "max_uses": None},
    {"id": 'LARPA_DOWNWARDS', "name": 'Downwards larpa', "type": 'MODIFIER', "mana": 120, "price": 290, "max_uses": None},
    {"id": 'LARPA_UPWARDS', "name": 'Upwards larpa', "type": 'MODIFIER', "mana": 120, "price": 290, "max_uses": None},
    {"id": 'LARPA_CHAOS_2', "name": 'Copy trail', "type": 'MODIFIER', "mana": 150, "price": 300, "max_uses": None},
    {"id": 'LARPA_DEATH', "name": 'Larpa Explosion', "type": 'MODIFIER', "mana": 90, "price": 150, "max_uses": 30},
    {"id": 'ALPHA', "name": 'Alpha', "type": 'OTHER', "mana": 30, "price": 200, "max_uses": None},
    {"id": 'GAMMA', "name": 'Gamma', "type": 'OTHER', "mana": 30, "price": 200, "max_uses": None},
    {"id": 'TAU', "name": 'Tau', "type": 'OTHER', "mana": 80, "price": 200, "max_uses": None},
    {"id": 'OMEGA', "name": 'Omega', "type": 'OTHER', "mana": 300, "price": 600, "max_uses": None},
    {"id": 'MU', "name": 'Mu', "type": 'OTHER', "mana": 120, "price": 500, "max_uses": None},
    {"id": 'PHI', "name": 'Phi', "type": 'OTHER', "mana": 120, "price": 500, "max_uses": None},
    {"id": 'SIGMA', "name": 'Sigma', "type": 'OTHER', "mana": 120, "price": 500, "max_uses": None},
    {"id": 'ZETA', "name": 'Zeta', "type": 'OTHER', "mana": 10, "price": 200, "max_uses": None},
    {"id": 'DIVIDE_2', "name": 'Divide by 2', "type": 'OTHER', "mana": 35, "price": 200, "max_uses": None},
    {"id": 'DIVIDE_3', "name": 'Divide by 3', "type": 'OTHER', "mana": 50, "price": 250, "max_uses": None},
    {"id": 'DIVIDE_4', "name": 'Divide by 4', "type": 'OTHER', "mana": 70, "price": 300, "max_uses": None},
    {"id": 'DIVIDE_10', "name": 'Divide by 10', "type": 'OTHER', "mana": 200, "price": 400, "max_uses": 5},
    {"id": 'METEOR_RAIN', "name": 'Meteorisade', "type": 'STATIC_PROJECTILE', "mana": 225, "price": 300, "max_uses": 2},
    {"id": 'WORM_RAIN', "name": 'Matosade', "type": 'STATIC_PROJECTILE', "mana": 225, "price": 300, "max_uses": 2},
    {"id": 'RESET', "name": 'Wand Refresh', "type": 'UTILITY', "mana": 20, "price": 120, "max_uses": None},
    {"id": 'IF_ENEMY', "name": 'Requirement - Enemies', "type": 'OTHER', "mana": 0, "price": 100, "max_uses": None},
    {"id": 'IF_PROJECTILE', "name": 'Requirement - Projectile Spells', "type": 'OTHER', "mana": 0, "price": 100, "max_uses": None},
    {"id": 'IF_HP', "name": 'Requirement - Low Health', "type": 'OTHER', "mana": 0, "price": 100, "max_uses": None},
    {"id": 'IF_HALF', "name": 'Requirement - Every Other', "type": 'OTHER', "mana": 0, "price": 100, "max_uses": None},
    {"id": 'IF_END', "name": 'Requirement - Endpoint', "type": 'OTHER', "mana": 0, "price": 10, "max_uses": None},
    {"id": 'IF_ELSE', "name": 'Requirement - Otherwise', "type": 'OTHER', "mana": 0, "price": 10, "max_uses": None},
    {"id": 'COLOUR_RED', "name": 'Red Glimmer', "type": 'MODIFIER', "mana": 0, "price": 40, "max_uses": None},
    {"id": 'COLOUR_ORANGE', "name": 'Orange Glimmer', "type": 'MODIFIER', "mana": 0, "price": 40, "max_uses": None},
    {"id": 'COLOUR_GREEN', "name": 'Green Glimmer', "type": 'MODIFIER', "mana": 0, "price": 40, "max_uses": None},
    {"id": 'COLOUR_YELLOW', "name": 'Yellow Glimmer', "type": 'MODIFIER', "mana": 0, "price": 40, "max_uses": None},
    {"id": 'COLOUR_PURPLE', "name": 'Purple Glimmer', "type": 'MODIFIER', "mana": 0, "price": 40, "max_uses": None},
    {"id": 'COLOUR_BLUE', "name": 'Blue Glimmer', "type": 'MODIFIER', "mana": 0, "price": 40, "max_uses": None},
    {"id": 'COLOUR_RAINBOW', "name": 'Rainbow Glimmer', "type": 'MODIFIER', "mana": 0, "price": 40, "max_uses": None},
    {"id": 'COLOUR_INVIS', "name": 'Invisible Spell', "type": 'MODIFIER', "mana": 0, "price": 40, "max_uses": None},
    {"id": 'RAINBOW_TRAIL', "name": 'Rainbow trail', "type": 'MODIFIER', "mana": 0, "price": 100, "max_uses": None},
]

SPELLS_BY_ID = {s["id"]: s for s in SPELLS}


def find_spell(query: str):
    """Looks up a spell by exact id, then exact name (case-insensitive), then falls back
    to a substring search over names/ids (which may return multiple matches)."""
    q = query.strip()
    if q.upper() in SPELLS_BY_ID:
        return SPELLS_BY_ID[q.upper()]
    ql = q.lower()
    exact_name = [s for s in SPELLS if s["name"].lower() == ql]
    if len(exact_name) == 1:
        return exact_name[0]
    matches = [s for s in SPELLS if ql in s["name"].lower() or ql in s["id"].lower()]
    return matches


def search_spells(query: str = "", type_filter: Optional[str] = None):
    ql = query.strip().lower()
    out = []
    for s in SPELLS:
        if type_filter and s["type"] != type_filter.upper():
            continue
        if ql and ql not in s["name"].lower() and ql not in s["id"].lower():
            continue
        out.append(s)
    out.sort(key=lambda s: s["name"])
    return out



GENERIC_SPELL_TEMPLATE = '<Entity \n        _version="1" \n        name="" \n        serialize="1" \n        tags="card_action" >\n\n        <_Transform \n          position.x="-1627.19" \n          position.y="-740.964" \n          rotation="0" \n          scale.x="1" \n          scale.y="1" >\n\n        </_Transform>\n\n        <HitboxComponent \n          _enabled="0" \n          _tags="enabled_in_world" \n          aabb_max_x="4" \n          aabb_max_y="3" \n          aabb_min_x="-4" \n          aabb_min_y="-3" \n          damage_multiplier="1" \n          is_enemy="1" \n          is_item="0" \n          is_player="0" \n          offset.x="0" \n          offset.y="0" >\n\n        </HitboxComponent>\n\n        <ItemActionComponent \n          _enabled="0" \n          _tags="enabled_in_world" \n          action_id="LASER_LUMINOUS_DRILL" >\n\n        </ItemActionComponent>\n\n        <ItemComponent \n          _enabled="0" \n          _tags="enabled_in_world" \n          always_use_item_name_in_ui="0" \n          auto_pickup="0" \n          camera_max_distance="50" \n          camera_smooth_speed_multiplier="1" \n          collect_nondefault_actions="0" \n          custom_pickup_string="" \n          drinkable="1" \n          enable_orb_hacks="0" \n          has_been_picked_by_player="0" \n          inventory_slot.x="4" \n          inventory_slot.y="0" \n          is_all_spells_book="0" \n          is_consumable="0" \n          is_equipable_forced="0" \n          is_frozen="0" \n          is_hittable_always="0" \n          is_identified="0" \n          is_pickable="1" \n          is_stackable="0" \n          item_name="" \n          item_pickup_radius="14.1" \n          mFramePickedUp="0" \n          max_child_items="0" \n          next_frame_pickable="136999" \n          npc_next_frame_pickable="0" \n          permanently_attached="0" \n          play_hover_animation="0" \n          play_pick_sound="1" \n          play_spinning_animation="0" \n          preferred_inventory="FULL" \n          remove_default_child_actions_on_death="0" \n          remove_on_death="0" \n          remove_on_death_if_empty="0" \n          spawn_pos.x="-1627.19" \n          spawn_pos.y="-740.964" \n          stats_count_as_item_pick_up="1" \n          ui_description="" \n          ui_display_description_on_pick_up_hint="0" \n          ui_sprite="" \n          uses_remaining="-1" >\n\n        </ItemComponent>\n\n        <SimplePhysicsComponent \n          _enabled="0" \n          _tags="enabled_in_world" \n          can_go_up="1" >\n\n        </SimplePhysicsComponent>\n\n        <SpriteComponent \n          _enabled="0" \n          _tags="enabled_in_world,item_identified" \n          additive="0" \n          alpha="1" \n          emissive="0" \n          fog_of_war_hole="0" \n          has_special_scale="0" \n          image_file="data/ui_gfx/gun_actions/luminous_drill_timer.png" \n          is_text_sprite="0" \n          kill_entity_after_finished="0" \n          never_ragdollify_on_death="0" \n          next_rect_animation="" \n          offset_animator_offset.x="0" \n          offset_animator_offset.y="0" \n          offset_x="8" \n          offset_y="17" \n          rect_animation="" \n          smooth_filtering="0" \n          special_scale_x="1" \n          special_scale_y="1" \n          text="" \n          transform_offset.x="0" \n          transform_offset.y="0" \n          ui_is_parent="0" \n          update_transform="1" \n          update_transform_rotation="1" \n          visible="1" \n          z_index="0.595" >\n\n        </SpriteComponent>\n\n        <SpriteComponent \n          _enabled="0" \n          _tags="enabled_in_world,item_unidentified" \n          additive="0" \n          alpha="1" \n          emissive="0" \n          fog_of_war_hole="0" \n          has_special_scale="0" \n          image_file="data/ui_gfx/gun_actions/unidentified.png" \n          is_text_sprite="0" \n          kill_entity_after_finished="0" \n          never_ragdollify_on_death="0" \n          next_rect_animation="" \n          offset_animator_offset.x="0" \n          offset_animator_offset.y="0" \n          offset_x="8" \n          offset_y="17" \n          rect_animation="" \n          smooth_filtering="0" \n          special_scale_x="1" \n          special_scale_y="1" \n          text="" \n          transform_offset.x="0" \n          transform_offset.y="0" \n          ui_is_parent="0" \n          update_transform="1" \n          update_transform_rotation="1" \n          visible="1" \n          z_index="0.595" >\n\n        </SpriteComponent>\n\n        <SpriteComponent \n          _enabled="0" \n          _tags="enabled_in_world,item_bg" \n          additive="0" \n          alpha="1" \n          emissive="0" \n          fog_of_war_hole="0" \n          has_special_scale="0" \n          image_file="data/ui_gfx/inventory/item_bg_projectile.png" \n          is_text_sprite="0" \n          kill_entity_after_finished="0" \n          never_ragdollify_on_death="0" \n          next_rect_animation="" \n          offset_animator_offset.x="0" \n          offset_animator_offset.y="0" \n          offset_x="10" \n          offset_y="19" \n          rect_animation="" \n          smooth_filtering="0" \n          special_scale_x="1" \n          special_scale_y="1" \n          text="" \n          transform_offset.x="0" \n          transform_offset.y="0" \n          ui_is_parent="0" \n          update_transform="1" \n          update_transform_rotation="1" \n          visible="1" \n          z_index="0.595" >\n\n        </SpriteComponent>\n\n        <SpriteOffsetAnimatorComponent \n          _enabled="0" \n          _tags="enabled_in_world" \n          sprite_id="0" \n          x_amount="0" \n          x_phase="16" \n          x_phase_offset="-221.837" \n          x_speed="0" \n          y_amount="1" \n          y_speed="2.5" >\n\n        </SpriteOffsetAnimatorComponent>\n\n        <SpriteOffsetAnimatorComponent \n          _enabled="0" \n          _tags="enabled_in_world" \n          sprite_id="1" \n          x_amount="0" \n          x_phase="16" \n          x_phase_offset="-221.837" \n          x_speed="0" \n          y_amount="1" \n          y_speed="2.5" >\n\n        </SpriteOffsetAnimatorComponent>\n\n        <SpriteOffsetAnimatorComponent \n          _enabled="0" \n          _tags="enabled_in_world" \n          sprite_id="2" \n          x_amount="0" \n          x_phase="16" \n          x_phase_offset="-221.837" \n          x_speed="0" \n          y_amount="1" \n          y_speed="2.5" >\n\n        </SpriteOffsetAnimatorComponent>\n\n        <SpriteOffsetAnimatorComponent \n          _enabled="0" \n          _tags="enabled_in_world" \n          sprite_id="3" \n          x_amount="0" \n          x_phase="16" \n          x_phase_offset="-221.837" \n          x_speed="0" \n          y_amount="1" \n          y_speed="2.5" >\n\n        </SpriteOffsetAnimatorComponent>\n\n        <VelocityComponent \n          _enabled="0" \n          _tags="enabled_in_world" \n          affect_physics_bodies="0" \n          air_friction="0.55" \n          apply_terminal_velocity="1" \n          displace_liquid="1" \n          gravity_x="0" \n          gravity_y="400" \n          limit_to_max_velocity="1" \n          liquid_death_threshold="0" \n          liquid_drag="1" \n          mVelocity.x="0" \n          mVelocity.y="0" \n          mass="0.05" \n          terminal_velocity="1000" \n          updates_velocity="1" >\n\n        </VelocityComponent>\n\n      </Entity>'




_OPEN_RE = re.compile(r"<Entity\b")
_CLOSE_RE = re.compile(r"</Entity>")
_ATTR_CACHE: dict = {}


def _attr(segment: str, name: str) -> Optional[str]:

    pattern = r'(?<![\w.])' + re.escape(name) + r'="([^"]*)"'
    m = re.search(pattern, segment)
    return m.group(1) if m else None


def _set_attr(text: str, name: str, value, count: int = 1) -> tuple:
    """Same word-boundary-safe matching as _attr, but for substitution. Returns
    (new_text, number_of_replacements_made)."""
    pattern = r'(?<![\w.])' + re.escape(name) + r'="[^"]*"'
    return re.subn(pattern, f'{name}="{value}"', text, count=count)


@dataclass
class EntityNode:
    start: int
    end: int  
    parent: Optional[int]  


def scan_entities(text: str) -> list[EntityNode]:
    """Stack-based scan that pairs every <Entity ...> with its matching </Entity>,
    without needing a full XML parser (which chokes on this file's odd \\r\\r\\n runs)."""
    tokens = []
    for m in _OPEN_RE.finditer(text):
        tokens.append((m.start(), "open", None))
    for m in _CLOSE_RE.finditer(text):
        tokens.append((m.start(), "close", m.end()))
    tokens.sort(key=lambda t: t[0])

    stack: list[int] = []
    entities: list[EntityNode] = []
    for pos, kind, end in tokens:
        if kind == "open":
            stack.append(pos)
        else:
            if not stack:
                continue  
            start = stack.pop()
            parent = stack[-1] if stack else None
            entities.append(EntityNode(start=start, end=end, parent=parent))
    return entities


@dataclass
class SpellSlot:
    start: int
    end: int
    action_id: Optional[str]
    slot_x: float
    slot_y: float

    @property
    def display(self):
        s = SPELLS_BY_ID.get(self.action_id)
        return s["name"] if s else (self.action_id or "(unknown)")

    @property
    def type(self):
        s = SPELLS_BY_ID.get(self.action_id)
        return s["type"] if s else "OTHER"


@dataclass
class Wand:
    start: int
    end: int
    ui_name: str
    mana: Optional[str]
    mana_max: Optional[str]
    deck_capacity: int
    spells: list = field(default_factory=list)


@dataclass
class PerkInfo:
    effect_id: Optional[str]     
    effect_start: Optional[int]
    effect_end: Optional[int]
    icon_id: Optional[str]       
    icon_start: Optional[int]
    icon_end: Optional[int]

    @property
    def display_id(self) -> str:
        return self.effect_id or (self.icon_id.upper() if self.icon_id else "UNKNOWN")

    @property
    def display_name(self) -> str:
        return self.display_id.replace("_", " ").title()



GENERIC_PERK_EFFECT_TEMPLATE = (
    '<Entity \n    _version="1" \n    name="" \n    serialize="1" \n    tags="perk_entity" >\n\n'
    '    <_Transform \n      position.x="0" \n      position.y="0" \n      rotation="0" \n'
    '      scale.x="1" \n      scale.y="1" >\n\n    </_Transform>\n\n'
    '    <GameEffectComponent \n      _enabled="1" \n      _tags="perk_component" \n'
    '      caused_by_ingestion_status_effect="0" \n      caused_by_stains="0" \n'
    '      causing_status_effect="NONE" \n      custom_effect_id="" \n      disable_movement="0" \n'
    '      effect="PROTECTION_EXPLOSION" \n      exclusivity_group="0" \n      frames="-1" \n'
    '      mCaster="0" \n      mCasterHerdId="0" \n      mCharmDisabledCameraBound="0" \n'
    '      mCharmEnabledTeleporting="0" \n      mCooldown="0" \n      mCounter="0" \n'
    '      mInvisible="0" \n      mIsExtension="0" \n      mIsSpent="0" \n      mSerializedData="" \n'
    '      no_heal_max_hp_cap="3.40282e+038" \n      polymorph_target="" \n      ragdoll_effect="NONE" \n'
    '      ragdoll_effect_custom_entity_file="" \n      ragdoll_fx_custom_entity_apply_only_to_largest_body="0" \n'
    '      ragdoll_material="air" \n      report_block_msg="1" \n      teleportation_delay_min_frames="30" \n'
    '      teleportation_probability="600" \n      teleportation_radius_max="1024" \n'
    '      teleportation_radius_min="128" \n      teleportations_num="0" >\n\n    </GameEffectComponent>\n\n'
    '    <InheritTransformComponent \n      _enabled="1" \n      always_use_immediate_parent_rotation="0" \n'
    '      only_position="0" \n      parent_hotspot_tag="" \n      parent_sprite_id="-1" \n'
    '      rotate_based_on_x_scale="0" \n      use_root_parent="0" >\n\n'
    '      <Transform \n        position.x="0" \n        position.y="0" \n        rotation="0" \n'
    '        scale.x="1" \n        scale.y="1" >\n\n      </Transform>\n\n    </InheritTransformComponent>\n\n'
    '  </Entity>'
)

GENERIC_PERK_ICON_TEMPLATE = (
    '<Entity \n    _version="1" \n    name="" \n    serialize="1" \n    tags="perk_entity" >\n\n'
    '    <_Transform \n      position.x="0" \n      position.y="0" \n      rotation="0" \n'
    '      scale.x="1" \n      scale.y="1" >\n\n    </_Transform>\n\n'
    '    <UIIconComponent \n      _enabled="1" \n      description="$perkdesc_protection_explosion" \n'
    '      display_above_head="0" \n      display_in_hud="1" \n'
    '      icon_sprite_file="data/ui_gfx/perk_icons/protection_explosion.png" \n      is_perk="1" \n'
    '      name="$perk_protection_explosion" >\n\n    </UIIconComponent>\n\n  </Entity>'
)



PERKS = [
    ("CRITICAL_HIT", "Critical Hit +"), ("BREATH_UNDERWATER", "Breathless"),
    ("EXTRA_MONEY", "Greed"), ("EXTRA_MONEY_TRICK_KILL", "Trick Greed"),
    ("HOVER_BOOST", "Strong Levitation"), ("MOVEMENT_FASTER", "Faster Movement"),
    ("LOW_GRAVITY", "Low Gravity"), ("SPEED_DIVER", "Fast Swimming"),
    ("STRONG_KICK", "Never Skip Leg Day"), ("REPELLING_CAPE", "Repelling Cape"),
    ("EXPLODING_CORPSES", "Exploding Corpses"), ("SAVING_GRACE", "Saving Grace"),
    ("INVISIBILITY", "Invisibility"), ("GLOBAL_GORE", "More Blood"),
    ("REMOVE_FOG_OF_WAR", "All-Seeing Eye"), ("VAMPIRISM", "Vampirism"),
    ("EXTRA_HP", "Extra Health"), ("HEARTS_MORE_EXTRA_HP", "Stronger Hearts"),
    ("GLASS_CANNON", "Glass Cannon"), ("RESPAWN", "Extra Life"),
    ("WORM_ATTRACTOR", "Worm Attractor"), ("WORM_DETRACTOR", "Worm Detractor"),
    ("PROTECTION_FIRE", "Fire Immunity"), ("PROTECTION_RADIOACTIVITY", "Toxic Immunity"),
    ("PROTECTION_EXPLOSION", "Explosion Immunity"), ("PROTECTION_MELEE", "Melee Immunity"),
    ("PROTECTION_ELECTRICITY", "Electricity Immunity"), ("TELEPORTITIS", "Teleportitis"),
    ("STAINLESS_ARMOUR", "Stainless Armour"), ("EDIT_WANDS_EVERYWHERE", "Tinker with Wands Everywhere"),
    ("ABILITY_ACTIONS_MATERIALIZED", "Bombs Materialized"), ("PROJECTILE_HOMING", "Homing Shots"),
    ("PROJECTILE_HOMING_SHOOTER", "Boomerang Spells"), ("FREEZE_FIELD", "Freeze Field"),
    ("DISSOLVE_POWDERS", "Dissolve Powders"), ("BLEED_SLIME", "Slime Blood"),
    ("BLEED_OIL", "Oil Blood"), ("SHIELD", "Permanent Shield"),
    ("REVENGE_EXPLOSION", "Revenge Explosion"), ("REVENGE_TENTACLE", "Revenge Tentacle"),
    ("ATTACK_FOOT", "Lukki Mutation"), ("PLAGUE_RATS", "Plague Rats"),
    ("PROJECTILE_REPULSION", "Projectile Repulsion Field"), ("ELECTRICITY", "Electricity"),
    ("ATTRACT_ITEMS", "Attract Gold"), ("EXTRA_KNOCKBACK", "Extra Knockback on Spells"),
    ("LOWER_SPREAD", "Concentrated Spells"), ("BOUNCE", "Bouncing Spells"),
    ("MYSTERY_EGGPLANT", "Eat Your Vegetables"), ("EXTRA_PERK", "Extra Perk"),
    ("PERKS_LOTTERY", "Perk Lottery"), ("GENOME_MORE_HATRED", "More Hatred"),
    ("GENOME_MORE_LOVE", "More Love"), ("FASTER_LEVITATION", "Faster Levitation"),
    ("EXTRA_SLOTS", "Extra Wand Capacity"), ("TELEKINESIS", "Telekinetic Kick"),
]
PERKS_BY_ID = {pid: name for pid, name in PERKS}


def find_perk(query: str):
    """Same contract as find_spell(): exact id/name match -> dict; ambiguous -> list;
    not found -> []. Also accepts a raw perk id not in PERKS at all, in case the person
    typed one straight from the wiki that isn't in our (non-exhaustive) local list."""
    q = query.strip()
    if not q:
        return []
    q_upper = q.upper().replace(" ", "_").replace("-", "_")
    if q_upper in PERKS_BY_ID:
        return {"id": q_upper, "name": PERKS_BY_ID[q_upper]}
    q_lower = q.lower()
    exact_name = [pid for pid, name in PERKS if name.lower() == q_lower]
    if len(exact_name) == 1:
        return {"id": exact_name[0], "name": PERKS_BY_ID[exact_name[0]]}
    starts = [pid for pid, name in PERKS if name.lower().startswith(q_lower)]
    if len(starts) == 1:
        return {"id": starts[0], "name": PERKS_BY_ID[starts[0]]}
    contains = [pid for pid, name in PERKS if q_lower in name.lower() or q_lower in pid.lower()]
    if len(contains) == 1:
        return {"id": contains[0], "name": PERKS_BY_ID[contains[0]]}
    matches = starts or contains
    if matches:
        return [{"id": pid, "name": PERKS_BY_ID[pid]} for pid in matches]

    if re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", q) and " " not in q:
        return {"id": q_upper, "name": q_upper.replace("_", " ").title()}
    return []


def search_perks(query: str = ""):
    q = query.strip().lower()
    if not q:
        return [{"id": pid, "name": name} for pid, name in PERKS]
    starts = [(pid, name) for pid, name in PERKS if name.lower().startswith(q) or pid.lower().startswith(q)]
    starts_ids = {pid for pid, _ in starts}
    contains = [(pid, name) for pid, name in PERKS
                if pid not in starts_ids and (q in name.lower() or q in pid.lower())]
    return [{"id": pid, "name": name} for pid, name in (starts + contains)]


class SaveEditor:
    """Loads a player.xml into memory, lets you inspect/edit wands, spells and basic
    stats, and writes the result back out. All edits operate on `self.text` as a plain
    string — nothing is re-serialized from a parsed tree, so formatting is preserved."""

    def __init__(self, path: str):
        self.path = Path(path)

        with open(self.path, "r", encoding="utf-8", newline="") as f:
            self.text = f.read()
        self._dirty = False



    def wands(self) -> list[Wand]:
        entities = scan_entities(self.text)
        by_start = {e.start: e for e in entities}
        wands = []
        for e in entities:
            head = self.text[e.start:e.start + 400]
            tags = (_attr(head, "tags") or "").split(",")
            if "wand" not in tags:
                continue
            seg = self.text[e.start:e.end]
            ui_name = _attr(seg, "ui_name") or "(unnamed wand)"
            mana = _attr(seg, "mana")
            mana_max = _attr(seg, "mana_max")
            deck_cap = int(_attr(seg, "deck_capacity") or 0)

            spells = []
            for c in entities:
                if c.parent != e.start:
                    continue
                cseg = self.text[c.start:c.end]
                ctags = (_attr(cseg, "tags") or "").split(",")
                if "card_action" not in ctags:
                    continue
                spells.append(SpellSlot(
                    start=c.start,
                    end=c.end,
                    action_id=_attr(cseg, "action_id"),
                    slot_x=float(_attr(cseg, "inventory_slot.x") or 0),
                    slot_y=float(_attr(cseg, "inventory_slot.y") or 0),
                ))
            spells.sort(key=lambda s: (s.slot_y, s.slot_x))
            wands.append(Wand(start=e.start, end=e.end, ui_name=ui_name, mana=mana,
                               mana_max=mana_max, deck_capacity=deck_cap, spells=spells))
        wands.sort(key=lambda w: w.start)
        return wands



    def _resolve_spell_id(self, spell: str) -> str:
        """Accepts either an exact action_id or a fuzzy name and returns a valid action_id,
        raising a clear error if it's ambiguous or not found."""
        result = find_spell(spell)
        if isinstance(result, dict):
            return result["id"]
        if isinstance(result, list):
            if len(result) == 1:
                return result[0]["id"]
            if len(result) == 0:
                raise ValueError(f'No spell found matching "{spell}". Try: noita_save_editor.py spells "{spell}"')
            names = ", ".join(f'{s["name"]} ({s["id"]})' for s in result[:8])
            raise ValueError(f'"{spell}" matches multiple spells: {names}{" ..." if len(result) > 8 else ""}. '
                              f'Use the exact spell id to disambiguate.')
        raise ValueError(f'Spell "{spell}" not recognized.')

    def swap_spell(self, wand_index: int, slot_index: int, new_spell: str) -> str:
        """wand_index and slot_index are both 1-based, matching the `list` output."""
        wand = self._get_wand(wand_index)
        if not (1 <= slot_index <= len(wand.spells)):
            raise ValueError(f"Wand {wand_index} ({wand.ui_name}) has {len(wand.spells)} spell(s); "
                              f"slot {slot_index} doesn't exist.")
        slot = wand.spells[slot_index - 1]
        new_id = self._resolve_spell_id(new_spell)
        self._replace_spell_block(slot, new_id)
        self._dirty = True
        return new_id

    def remove_spell(self, wand_index: int, slot_index: int) -> str:
        wand = self._get_wand(wand_index)
        if not (1 <= slot_index <= len(wand.spells)):
            raise ValueError(f"Wand {wand_index} ({wand.ui_name}) has {len(wand.spells)} spell(s); "
                              f"slot {slot_index} doesn't exist.")
        slot = wand.spells[slot_index - 1]
        removed_id = slot.action_id
        self.text = self.text[:slot.start] + self.text[slot.end:]
        self._dirty = True
        return removed_id

    def add_spell(self, wand_index: int, new_spell: str) -> str:
        wand = self._get_wand(wand_index)
        if len(wand.spells) >= wand.deck_capacity:
            raise ValueError(f"Wand {wand_index} ({wand.ui_name}) is at capacity "
                              f"({wand.deck_capacity} spells) — remove one first.")
        new_id = self._resolve_spell_id(new_spell)
        next_slot = (max((s.slot_x for s in wand.spells)) + 1) if wand.spells else 0

        if wand.spells:
            template = self.text[wand.spells[0].start:wand.spells[0].end]
        else:
            template = _generic_spell_template()

        spec = SPELLS_BY_ID.get(new_id)
        new_uses = str(spec["max_uses"]) if spec and spec["max_uses"] is not None else "-1"

        block = re.sub(r'action_id="[^"]*"', f'action_id="{new_id}"', template, count=1)
        block = re.sub(r'uses_remaining="[^"]*"', f'uses_remaining="{new_uses}"', block, count=1)
        block = re.sub(r'inventory_slot\.x="[^"]*"', f'inventory_slot.x="{int(next_slot)}"', block, count=1)

        insert_at = wand.end - len("</Entity>")
        self.text = self.text[:insert_at] + block + self.text[insert_at:]
        self._dirty = True
        return new_id

    def _replace_spell_block(self, slot: SpellSlot, new_id: str):
        block = self.text[slot.start:slot.end]
        spec = SPELLS_BY_ID.get(new_id)
        new_uses = str(spec["max_uses"]) if spec and spec["max_uses"] is not None else "-1"
        block = re.sub(r'action_id="[^"]*"', f'action_id="{new_id}"', block, count=1)
        block = re.sub(r'uses_remaining="[^"]*"', f'uses_remaining="{new_uses}"', block, count=1)
        self.text = self.text[:slot.start] + block + self.text[slot.end:]

    def _get_wand(self, wand_index: int) -> Wand:
        wands = self.wands()
        if not (1 <= wand_index <= len(wands)):
            raise ValueError(f"There are {len(wands)} wand(s) in this save; wand {wand_index} doesn't exist.")
        return wands[wand_index - 1]



    def get_health(self):
        m = re.search(r"<DamageModelComponent\b.*?\bhp=\"([^\"]*)\"", self.text, re.S)
        m2 = re.search(r"<DamageModelComponent\b.*?\bmax_hp=\"([^\"]*)\"", self.text, re.S)
        return (float(m.group(1)) if m else None, float(m2.group(1)) if m2 else None)

    def set_health(self, hp: Optional[float] = None, max_hp: Optional[float] = None):
        if hp is not None:
            self.text = re.sub(r'(<DamageModelComponent\b.*?\bhp=")[^"]*(")',
                                lambda m: m.group(1) + repr(float(hp)) + m.group(2),
                                self.text, count=1, flags=re.S)
            self._dirty = True
        if max_hp is not None:

            for attr in ("max_hp", "max_hp_cap", "max_hp_old"):
                self.text = re.sub(rf'(<DamageModelComponent\b.*?\b{attr}=")[^"]*(")',
                                    lambda m: m.group(1) + repr(float(max_hp)) + m.group(2),
                                    self.text, count=1, flags=re.S)
            self._dirty = True

    def get_money(self):
        m = re.search(r'<WalletComponent\b.*?\bmoney="([^"]*)"', self.text, re.S)
        return int(m.group(1)) if m else None

    def set_money(self, amount: int):
        self.text = re.sub(r'(<WalletComponent\b.*?\bmoney=")[^"]*(")',
                            lambda m: m.group(1) + str(int(amount)) + m.group(2),
                            self.text, count=1, flags=re.S)
        self._dirty = True



    WAND_STAT_FIELDS = ("mana", "mana_max", "mana_charge_speed", "actions_per_round",
                        "reload_time", "fire_rate_wait")

    WAND_STAT_LABELS = {
        "mana": "Current mana",
        "mana_max": "Max mana",
        "mana_charge_speed": "Mana charge speed",
        "actions_per_round": "Spells cast at once",
        "reload_time": "Recharge time (frames)",
        "fire_rate_wait": "Cast delay (frames)",
    }

    def get_wand_stats(self, wand_index: int) -> dict:
        wand = self._get_wand(wand_index)
        seg = self.text[wand.start:wand.end]
        return {field: _attr(seg, field) for field in self.WAND_STAT_FIELDS}

    def set_wand_stat(self, wand_index: int, field: str, value) -> None:
        if field not in self.WAND_STAT_FIELDS:
            raise ValueError(f"Unknown wand stat {field!r}.")
        wand = self._get_wand(wand_index)
        seg = self.text[wand.start:wand.end]
        new_seg, n = _set_attr(seg, field, value, count=1)
        if n == 0:
            raise ValueError(f"Couldn't find {field!r} on wand {wand_index} ({wand.ui_name}).")
        self.text = self.text[:wand.start] + new_seg + self.text[wand.end:]
        self._dirty = True



    def perks(self) -> list["PerkInfo"]:
        entities = scan_entities(self.text)
        effects, icons = [], []
        for e in entities:
            head = self.text[e.start:e.start + 300]
            tags = (_attr(head, "tags") or "").split(",")
            if "perk_entity" not in tags:
                continue
            seg = self.text[e.start:e.end]
            if "<GameEffectComponent" in seg:
                effects.append((_attr(seg, "effect"), e.start, e.end))
            elif "<UIIconComponent" in seg:
                m = re.search(r'(?<![\w.])name="\$perk_([^"]*)"', seg)
                icon_id = m.group(1) if m else None
                icons.append((icon_id, e.start, e.end))

        perks = []
        used = set()
        for eff_id, es, ee in effects:
            match_i = None
            for i, (icon_id, is_, ie) in enumerate(icons):
                if i in used:
                    continue
                if icon_id and eff_id and icon_id.upper() == eff_id.upper():
                    match_i = i
                    break
            if match_i is not None:
                used.add(match_i)
                icon_id, is_, ie = icons[match_i]
                perks.append(PerkInfo(eff_id, es, ee, icon_id, is_, ie))
            else:
                perks.append(PerkInfo(eff_id, es, ee, None, None, None))
        for i, (icon_id, is_, ie) in enumerate(icons):
            if i in used:
                continue
            perks.append(PerkInfo(None, None, None, icon_id, is_, ie))

        perks.sort(key=lambda p: p.effect_start if p.effect_start is not None else p.icon_start)
        return perks

    def remove_perk(self, perk_index: int) -> str:
        """perk_index is 1-based, matching how wands/slots are numbered elsewhere."""
        perks = self.perks()
        if not (1 <= perk_index <= len(perks)):
            raise ValueError(f"There are {len(perks)} perk(s) in this save; perk {perk_index} doesn't exist.")
        p = perks[perk_index - 1]
        spans = [s for s in [(p.effect_start, p.effect_end), (p.icon_start, p.icon_end)] if s[0] is not None]
        spans.sort(key=lambda s: s[0], reverse=True)  
        for start, end in spans:
            self.text = self.text[:start] + self.text[end:]
        self._dirty = True
        return p.display_id

    def add_perk(self, perk: str) -> str:
        result = find_perk(perk)
        if isinstance(result, list):
            if len(result) == 0:
                raise ValueError(f'No perk found matching "{perk}".')
            names = ", ".join(f'{p["name"]} ({p["id"]})' for p in result[:8])
            raise ValueError(f'"{perk}" matches multiple perks: {names}{" ..." if len(result) > 8 else ""}. '
                              f'Use the exact perk id to disambiguate.')
        perk_id = result["id"]
        lower = perk_id.lower()

        existing = self.perks()
        effect_template = icon_template = None
        for p in existing:
            if effect_template is None and p.effect_start is not None:
                effect_template = self.text[p.effect_start:p.effect_end]
            if icon_template is None and p.icon_start is not None:
                icon_template = self.text[p.icon_start:p.icon_end]
            if effect_template and icon_template:
                break
        if effect_template is None:
            effect_template = GENERIC_PERK_EFFECT_TEMPLATE
        if icon_template is None:
            icon_template = GENERIC_PERK_ICON_TEMPLATE

        effect_block, _ = _set_attr(effect_template, "effect", perk_id, count=1)

        icon_block = re.sub(r'(?<![\w.])name="\$perk_[^"]*"', f'name="$perk_{lower}"', icon_template, count=1)
        icon_block = re.sub(r'(?<![\w.])description="\$perkdesc_[^"]*"', f'description="$perkdesc_{lower}"',
                             icon_block, count=1)
        icon_block, _ = _set_attr(icon_block, "icon_sprite_file", f'data/ui_gfx/perk_icons/{lower}.png', count=1)

        if existing:
            insertion_point = max(max(p.effect_end or 0, p.icon_end or 0) for p in existing)
        else:
            insertion_point = self.text.rfind("</Entity>")
            if insertion_point == -1:
                raise ValueError("Could not find a place to insert the new perk in this save.")

        block = "\n\n  " + effect_block + "\n\n  " + icon_block
        self.text = self.text[:insertion_point] + block + self.text[insertion_point:]
        self._dirty = True
        return perk_id


    def save(self, out_path: Optional[str] = None, backup: bool = True, in_place: bool = False):
        if in_place:
            target = self.path
        elif out_path:
            target = Path(out_path)
        else:
            target = self.path.with_name(self.path.stem + "_edited" + self.path.suffix)

        if backup and target == self.path:
            bak = self.path.with_suffix(self.path.suffix + ".bak")
            if not bak.exists():
                shutil.copy2(self.path, bak)

        with open(target, "w", encoding="utf-8", newline="") as f:
            f.write(self.text)
        return target


def _generic_spell_template() -> str:
    if GENERIC_SPELL_TEMPLATE is not None:
        return GENERIC_SPELL_TEMPLATE
    raise ValueError(
        "This wand has no spells to use as a template, and no bundled fallback template "
        "is available. Add a spell to a different wand in the same save first, or swap into "
        "an existing (even wrong) spell slot instead of adding a new one."
    )



import tkinter as tk
from tkinter import ttk, filedialog, messagebox

TYPE_LABELS = {
    "PROJECTILE": "Projectile", "STATIC_PROJECTILE": "Static", "MODIFIER": "Modifier",
    "DRAW_MANY": "Multicast", "MATERIAL": "Material", "UTILITY": "Utility",
    "PASSIVE": "Passive", "OTHER": "Other",
}

BG = "#0b0a10"
PANEL = "#161328"
PANEL2 = "#1c1930"
LINE = "#3a3455"
GOLD = "#c9a24b"
TEXT = "#e9e4d8"
TEXT_DIM = "#a49cc4"
GLOW = "#7ee0c9"
DANGER = "#e39d84"

FONT_H1 = ("Georgia", 18)
FONT_H2 = ("Georgia", 12)
FONT_BODY = ("Segoe UI", 9)
FONT_MONO = ("Consolas", 9)


class Autocomplete:
    """An Entry with a filtered dropdown, shown in a small borderless popup window
    positioned under the entry. Works for spells or perks depending on which
    search_fn/find_fn/label_fn are passed in — both use {"id":..., "name":...} items."""

    def __init__(self, master, on_select, initial="", search_fn=None, find_fn=None, label_fn=None):
        self.master = master
        self.on_select = on_select
        self.search_fn = search_fn or (lambda q: search_spells(q)[:30])
        self.find_fn = find_fn or find_spell
        self.label_fn = label_fn or (
            lambda s: f'{s["name"]}  ·  {TYPE_LABELS.get(s.get("type"), s.get("type"))}  ·  {s.get("mana")}mp')
        self.var = tk.StringVar(value=initial)
        self.entry = tk.Entry(master, textvariable=self.var, width=34,
                               bg="#0f0d18", fg=TEXT, insertbackground=TEXT,
                               relief="flat", highlightthickness=1,
                               highlightbackground=LINE, highlightcolor=GLOW,
                               font=FONT_BODY)
        self.popup = None
        self.listbox = None
        self.results = []
        self._suppress = False

        self.var.trace_add("write", self._on_change)
        self.entry.bind("<Down>", self._focus_listbox)
        self.entry.bind("<Return>", self._on_enter)
        self.entry.bind("<Escape>", lambda e: self._hide())
        self.entry.bind("<FocusOut>", lambda e: self.entry.after(150, self._hide))

    def grid(self, **kw):
        self.entry.grid(**kw)

    def pack(self, **kw):
        self.entry.pack(**kw)

    def set_text(self, text):
        self._suppress = True
        self.var.set(text)
        self._suppress = False

    def _on_change(self, *_args):
        if self._suppress:
            return
        text = self.var.get().strip()
        if not text:
            self._hide()
            return
        self.results = self.search_fn(text)[:30]
        if self.results:
            self._show()
        else:
            self._hide()

    def _show(self):
        if self.popup is None:
            self.popup = tk.Toplevel(self.entry)
            self.popup.wm_overrideredirect(True)
            self.popup.configure(bg=LINE)
            self.listbox = tk.Listbox(self.popup, bg="#141020", fg=TEXT,
                                       selectbackground="#3a3455",
                                       selectforeground=TEXT,
                                       relief="flat", highlightthickness=0,
                                       font=FONT_BODY, activestyle="none")
            self.listbox.pack(fill="both", expand=True, padx=1, pady=1)
            self.listbox.bind("<<ListboxSelect>>", self._on_listbox_pick)
            self.listbox.bind("<Return>", self._on_listbox_pick)
            self.listbox.bind("<Escape>", lambda e: self._hide())
        self.listbox.delete(0, "end")
        for s in self.results:
            self.listbox.insert("end", self.label_fn(s))
        height = min(8, len(self.results))
        self.listbox.configure(height=height)
        self.entry.update_idletasks()
        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height()
        w = max(self.entry.winfo_width(), 300)
        self.popup.geometry(f"{w}x{height * 20 + 4}+{x}+{y}")
        self.popup.deiconify()
        self.popup.lift()

    def _hide(self):
        if self.popup is not None:
            self.popup.withdraw()

    def _focus_listbox(self, _event):
        if self.popup and self.results:
            self.listbox.focus_set()
            self.listbox.selection_set(0)

    def _on_listbox_pick(self, _event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        self._choose(self.results[sel[0]])

    def _on_enter(self, _event):
        text = self.var.get().strip()
        if not text:
            return
        result = self.find_fn(text)
        if isinstance(result, dict):
            self._choose(result)
        elif isinstance(result, list) and len(result) == 1:
            self._choose(result[0])
        elif self.results:
            self._choose(self.results[0])

    def _choose(self, item):
        self.set_text(item["name"])
        self._hide()
        self.on_select(item["id"])


class NoitaEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wand & Sigil — Noita Save Editor")
        self.geometry("880x720")
        self.minsize(680, 480)
        self.configure(bg=BG)

        self.editor: SaveEditor | None = None
        self.autocompletes = []  
        self.wand_stat_vars = {}  

        self._build_menu()
        self._build_layout()
        self._show_empty_state()


    def _build_menu(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open player.xml...", command=self.open_file, accelerator="Ctrl+O")
        filemenu.add_separator()
        filemenu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        filemenu.add_command(label="Save As...", command=self.save_file_as, accelerator="Ctrl+Shift+S")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)
        self.bind_all("<Control-o>", lambda e: self.open_file())
        self.bind_all("<Control-s>", lambda e: self.save_file())
        self.bind_all("<Control-S>", lambda e: self.save_file_as())


    def _build_layout(self):
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=18, pady=(16, 6))
        tk.Label(header, text="Wand & Sigil", font=FONT_H1, bg=BG, fg=GOLD).pack(anchor="w")
        tk.Label(header, text="Edit wands, spells, health and money in a Noita player.xml save.",
                 font=FONT_BODY, bg=BG, fg=TEXT_DIM).pack(anchor="w")

        self.filebar = tk.Frame(self, bg=PANEL)
        self.filebar.pack(fill="x", padx=18, pady=6)
        self.fname_label = tk.Label(self.filebar, text="No file loaded", bg=PANEL, fg=GLOW,
                                     font=FONT_MONO, anchor="w")
        self.fname_label.pack(side="left", padx=12, pady=10)
        btnframe = tk.Frame(self.filebar, bg=PANEL)
        btnframe.pack(side="right", padx=10, pady=8)
        self._mkbutton(btnframe, "Open...", self.open_file).pack(side="left", padx=4)
        self.save_btn = self._mkbutton(btnframe, "Save", self.save_file, primary=True)
        self.save_btn.pack(side="left", padx=4)
        self.save_btn.configure(state="disabled")


        self.stats_frame = tk.LabelFrame(self, text="Vitals", bg=PANEL, fg=GOLD,
                                          font=FONT_H2, labelanchor="nw", bd=1,
                                          highlightbackground=LINE, highlightthickness=1)
        self.stats_frame.pack(fill="x", padx=18, pady=8)
        self.hp_var = tk.StringVar()
        self.maxhp_var = tk.StringVar()
        self.money_var = tk.StringVar()
        self._stat_field(self.stats_frame, "Health", self.hp_var, 0)
        self._stat_field(self.stats_frame, "Max health", self.maxhp_var, 1)
        self._stat_field(self.stats_frame, "Money", self.money_var, 2)
        self._mkbutton(self.stats_frame, "Apply", self._apply_stats).grid(row=0, column=6, rowspan=2, padx=14)


        self.perks_frame = tk.LabelFrame(self, text="Perks", bg=PANEL, fg=GOLD,
                                          font=FONT_H2, labelanchor="nw", bd=1,
                                          highlightbackground=LINE, highlightthickness=1)
        self.perks_frame.pack(fill="x", padx=18, pady=8)
        self.perks_list_frame = tk.Frame(self.perks_frame, bg=PANEL)
        self.perks_list_frame.pack(fill="x", padx=10, pady=(10, 4))
        add_perk_row = tk.Frame(self.perks_frame, bg=PANEL)
        add_perk_row.pack(fill="x", padx=10, pady=(2, 10))
        self.perk_autocomplete = Autocomplete(
            add_perk_row, on_select=self._do_add_perk, initial="",
            search_fn=lambda q: search_perks(q)[:30],
            find_fn=find_perk,
            label_fn=lambda p: p["name"],
        )
        self.perk_autocomplete.pack(side="left")
        tk.Label(add_perk_row, text="  search by name (e.g. \"faster levitation\") or type a raw perk id",
                 bg=PANEL, fg=TEXT_DIM, font=FONT_BODY).pack(side="left")

        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True, padx=18, pady=(4, 8))
        self.canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        vsb = ttk.Scrollbar(outer, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.wands_frame = tk.Frame(self.canvas, bg=BG)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.wands_frame, anchor="nw")
        self.wands_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)


        self.status_var = tk.StringVar(value="Open a player.xml file to begin.")
        status = tk.Label(self, textvariable=self.status_var, bg=BG, fg=TEXT_DIM,
                           font=FONT_MONO, anchor="w")
        status.pack(fill="x", padx=20, pady=(0, 10))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _stat_field(self, parent, label, var, col):
        tk.Label(parent, text=label, bg=PANEL, fg=TEXT_DIM, font=FONT_BODY).grid(
            row=0, column=col * 2, sticky="w", padx=(14 if col else 14, 4), pady=(10, 0))
        e = tk.Entry(parent, textvariable=var, width=12, bg="#0f0d18", fg=TEXT,
                     insertbackground=TEXT, relief="flat", highlightthickness=1,
                     highlightbackground=LINE, highlightcolor=GLOW, font=FONT_MONO)
        e.grid(row=1, column=col * 2, sticky="w", padx=(14 if col else 14, 4), pady=(2, 10))

    def _mkbutton(self, parent, text, command, primary=False, danger=False):
        bg = GOLD if primary else ("#2e1912" if danger else "#231e38")
        fg = "#1a1508" if primary else (DANGER if danger else TEXT)
        b = tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                      activebackground=bg, activeforeground=fg, relief="flat",
                      font=FONT_BODY, padx=10, pady=4, bd=0, cursor="hand2",
                      highlightthickness=1, highlightbackground=LINE)
        return b

    def _show_empty_state(self):
        for w in self.wands_frame.winfo_children():
            w.destroy()
        tk.Label(self.wands_frame, text="No save loaded yet.", bg=BG, fg=TEXT_DIM,
                 font=FONT_BODY).pack(anchor="w", pady=20)



    def open_file(self):
        path = filedialog.askopenfilename(
            title="Open Noita player.xml",
            filetypes=[("Noita save (player.xml)", "player.xml"), ("XML files", "*.xml"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            self.editor = SaveEditor(path)
        except Exception as exc:  
            messagebox.showerror("Couldn't open file", str(exc))
            return
        self.fname_label.configure(text=path)
        self.save_btn.configure(state="normal")
        self.status_var.set(f"Loaded {path}")
        self.render()

    def save_file(self):
        if not self.editor:
            return
        try:
            out = self.editor.save(in_place=True, backup=True)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Couldn't save", str(exc))
            return
        self.status_var.set(f"Saved to {out} (backup kept as {out}.bak the first time).")

    def save_file_as(self):
        if not self.editor:
            return
        path = filedialog.asksaveasfilename(
            title="Save edited save as...", defaultextension=".xml",
            initialfile=self.editor.path.stem + "_edited.xml",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            out = self.editor.save(out_path=path, backup=False)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Couldn't save", str(exc))
            return
        self.status_var.set(f"Saved to {out}")



    def render(self):
        if not self.editor:
            return
        hp, max_hp = self.editor.get_health()
        self.hp_var.set("" if hp is None else _fmt_num(hp))
        self.maxhp_var.set("" if max_hp is None else _fmt_num(max_hp))
        money = self.editor.get_money()
        self.money_var.set("" if money is None else str(money))
        self._render_perks()

        for w in self.wands_frame.winfo_children():
            w.destroy()
        self.autocompletes.clear()
        self.wand_stat_vars = {}

        wands = self.editor.wands()
        if not wands:
            tk.Label(self.wands_frame, text="No wands found in this save.", bg=BG, fg=TEXT_DIM,
                     font=FONT_BODY).pack(anchor="w", pady=20)
            return

        for wi, wand in enumerate(wands):
            self._render_wand(wi, wand)

    def _render_perks(self):
        for w in self.perks_list_frame.winfo_children():
            w.destroy()
        perks = self.editor.perks()
        if not perks:
            tk.Label(self.perks_list_frame, text="No perks picked up yet.", bg=PANEL, fg=TEXT_DIM,
                     font=FONT_BODY).pack(anchor="w")
            return
        for i, p in enumerate(perks):
            row = tk.Frame(self.perks_list_frame, bg=PANEL)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=p.display_name, bg=PANEL, fg=TEXT, font=FONT_BODY,
                     width=26, anchor="w").pack(side="left")
            tk.Label(row, text=p.display_id, bg=PANEL, fg=TEXT_DIM, font=FONT_MONO,
                     anchor="w").pack(side="left", padx=(0, 10))
            self._mkbutton(row, "Remove", lambda i=i: self._do_remove_perk(i), danger=True).pack(side="left")

    def _render_wand(self, wi, wand):
        mana_txt = "—"
        if wand.mana is not None and wand.mana_max is not None:
            try:
                mana_txt = f"{int(float(wand.mana))} / {int(float(wand.mana_max))}"
            except ValueError:
                mana_txt = f"{wand.mana} / {wand.mana_max}"
        title = f"Wand {wi + 1} — {wand.ui_name}   (mana {mana_txt} · capacity {wand.deck_capacity} · {len(wand.spells)} spell(s))"
        frame = tk.LabelFrame(self.wands_frame, text=title, bg=PANEL, fg=GOLD, font=FONT_BODY,
                               labelanchor="nw", bd=1, highlightbackground=LINE, highlightthickness=1)
        frame.pack(fill="x", pady=6)

        stats = self.editor.get_wand_stats(wi + 1)
        stat_row = tk.Frame(frame, bg=PANEL)
        stat_row.pack(fill="x", padx=10, pady=(6, 8))
        self.wand_stat_vars[wi] = {}
        stat_fields = ("fire_rate_wait", "actions_per_round", "reload_time", "mana_max", "mana_charge_speed")
        for field in stat_fields:
            var = tk.StringVar(value=stats.get(field) or "")
            self.wand_stat_vars[wi][field] = var
            sub = tk.Frame(stat_row, bg=PANEL)
            sub.pack(side="left", padx=(0, 14))
            tk.Label(sub, text=SaveEditor.WAND_STAT_LABELS[field], bg=PANEL, fg=TEXT_DIM,
                     font=FONT_BODY).pack(anchor="w")
            e = tk.Entry(sub, textvariable=var, width=10, bg="#0f0d18", fg=TEXT,
                         insertbackground=TEXT, relief="flat", highlightthickness=1,
                         highlightbackground=LINE, highlightcolor=GLOW, font=FONT_MONO)
            e.pack(anchor="w")
        self._mkbutton(stat_row, "Apply", lambda wi=wi: self._apply_wand_stats(wi),
                        primary=True).pack(side="left", padx=(4, 0), pady=(16, 0))

        for si, slot in enumerate(wand.spells):
            row = tk.Frame(frame, bg=PANEL)
            row.pack(fill="x", padx=10, pady=3)
            tk.Label(row, text=f"{si + 1}.", bg=PANEL, fg=TEXT_DIM, font=FONT_MONO, width=3, anchor="e").pack(side="left")
            tk.Label(row, text=TYPE_LABELS.get(slot.type, slot.type), bg=PANEL, fg=TEXT_DIM,
                     font=FONT_MONO, width=11, anchor="w").pack(side="left", padx=(4, 8))
            ac = Autocomplete(row, on_select=lambda new_id, wi=wi, si=si: self._do_swap(wi, si, new_id),
                               initial=slot.display)
            ac.pack(side="left")
            self.autocompletes.append(ac)
            self._mkbutton(row, "Remove", lambda wi=wi, si=si: self._do_remove(wi, si),
                            danger=True).pack(side="left", padx=8)

        add_row = tk.Frame(frame, bg=PANEL)
        add_row.pack(fill="x", padx=10, pady=(6, 10))
        at_capacity = len(wand.spells) >= wand.deck_capacity
        ac = Autocomplete(add_row, on_select=lambda new_id, wi=wi: self._do_add(wi, new_id), initial="")
        ac.pack(side="left")
        self.autocompletes.append(ac)
        if at_capacity:
            ac.entry.configure(state="disabled")
            tk.Label(add_row, text="  wand is at capacity — remove a spell first",
                     bg=PANEL, fg=TEXT_DIM, font=FONT_BODY).pack(side="left")
        else:
            tk.Label(add_row, text="  ← add a spell", bg=PANEL, fg=TEXT_DIM, font=FONT_BODY).pack(side="left")


    def _do_swap(self, wand_index, slot_index, new_id):
        try:
            self.editor.swap_spell(wand_index + 1, slot_index + 1, new_id)
            self.status_var.set(f"Wand {wand_index + 1}, slot {slot_index + 1} -> {new_id}")
        except ValueError as exc:
            messagebox.showerror("Couldn't swap spell", str(exc))
        self.render()

    def _do_remove(self, wand_index, slot_index):
        try:
            removed = self.editor.remove_spell(wand_index + 1, slot_index + 1)
            self.status_var.set(f"Removed {removed} from wand {wand_index + 1}, slot {slot_index + 1}")
        except ValueError as exc:
            messagebox.showerror("Couldn't remove spell", str(exc))
        self.render()

    def _do_add(self, wand_index, new_id):
        try:
            self.editor.add_spell(wand_index + 1, new_id)
            self.status_var.set(f"Added {new_id} to wand {wand_index + 1}")
        except ValueError as exc:
            messagebox.showerror("Couldn't add spell", str(exc))
        self.render()

    def _apply_stats(self):
        if not self.editor:
            return
        try:
            hp = float(self.hp_var.get()) if self.hp_var.get().strip() else None
            max_hp = float(self.maxhp_var.get()) if self.maxhp_var.get().strip() else None
            money = int(float(self.money_var.get())) if self.money_var.get().strip() else None
        except ValueError:
            messagebox.showerror("Invalid value", "Health, max health and money must be numbers.")
            return
        if hp is not None or max_hp is not None:
            self.editor.set_health(hp=hp, max_hp=max_hp)
        if money is not None:
            self.editor.set_money(money)
        self.status_var.set("Vitals updated — remember to Save.")
        self.render()

    def _apply_wand_stats(self, wand_index):
        if not self.editor:
            return
        field_vars = self.wand_stat_vars.get(wand_index, {})
        updates = {}
        for field, var in field_vars.items():
            txt = var.get().strip()
            if not txt:
                continue
            try:
                float(txt)
            except ValueError:
                messagebox.showerror("Invalid value",
                                      f"{SaveEditor.WAND_STAT_LABELS[field]} must be a number (got {txt!r}).")
                return
            updates[field] = txt
        try:
            for field, txt in updates.items():
                self.editor.set_wand_stat(wand_index + 1, field, txt)
        except ValueError as exc:
            messagebox.showerror("Couldn't update wand", str(exc))
            return
        self.status_var.set(f"Wand {wand_index + 1} stats updated — remember to Save.")
        self.render()

    def _do_add_perk(self, perk_id):
        if not self.editor:
            return
        try:
            new_id = self.editor.add_perk(perk_id)
        except ValueError as exc:
            messagebox.showerror("Couldn't add perk", str(exc))
            return
        self.status_var.set(
            f"Added perk {new_id}. Note: a few perks run one-time setup logic when first "
            f"picked up in-game (e.g. permanently resizing a wand) rather than only being "
            f"this always-on effect — those may not fully replicate. Simple passive/immunity "
            f"perks like this should work correctly. Verify in-game and keep your backup."
        )
        self.render()

    def _do_remove_perk(self, perk_index):
        if not self.editor:
            return
        try:
            removed = self.editor.remove_perk(perk_index + 1)
            self.status_var.set(f"Removed perk {removed}.")
        except ValueError as exc:
            messagebox.showerror("Couldn't remove perk", str(exc))
        self.render()


def _fmt_num(x: float) -> str:
    return str(int(x)) if float(x).is_integer() else str(x)


def main():
    app = NoitaEditorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
