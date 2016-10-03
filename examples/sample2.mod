BEGIN, , ;
CREATE, 1, 0, Part1: 30, ;
COUNT: Part1, ;
DELAY: 2, : DrillStation;
CREATE, 1, 0, Part2: 20, ;
COUNT: Part2, ;
DELAY: 10, ;
DrillStation	QUEUE, Drill.Queue, , ;
            	SEIZE, : Drill, 1;
            	DELAY: NORM(10,1), ;
            	RELEASE: Drill, ;

Branch, 1, : If, Entity.Type==Part1, StraightenerStation:
		ELSE, , FinishStation;
StraightenerStation	QUEUE, Straighten.Queue, , ;
                   	SEIZE, : Straightener, ;
                   	DELAY: EXPO(15), ;
                   	RELEASE: Straightener, ;

FinishStation	QUEUE, Finish.Queue, , ;
             	SEIZE, : Finisher, ;
             	DELAY: 5, ;
             	RELEASE: Finisher, ;

COUNT: TotalEntities, ;
DISPOSE;
END;