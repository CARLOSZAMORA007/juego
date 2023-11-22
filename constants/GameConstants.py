import enum
class GameConstants(enum.Enum):
    MAX_LEVELS=5
    LANES=3
    
    INITIAL_ENERGY=100
    MAX_ENERGY=500
    
    PROJ_INITIAL_VEL=2
    PROJ_ACELERATION=1
    
    ENEMY_VEL=0.3
    VILLAIN_ACTIONS=["enemy", "move", "stop", "good"]
    VILLAIN_INTIAL_ACTION="stop"
    
    VILLAIN_MOVE=[-1, 1]
    ENEMY_MOVE=[-1, 0, 1]
    
    ITEM_GRAVITY=1
    ITEMS_POWERS=["frezee", "double", "energy"]
    
    DAMAGE_SHOT=20
    
    HITS_COUNT=3
    FREEZE_COUNT_FLAG=10
    
    OBJ_THREAD_TIME=0.002