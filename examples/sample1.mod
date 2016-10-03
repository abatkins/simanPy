BEGIN, , ;
CREATE, , , : EXPO(4.4), ;
QUEUE, Buffer, 100, ;
SEIZE, : Machine, ;
DELAY: TRIA(3.2,4.2,5.2), ;
RELEASE: Machine, ;
COUNT: JobsDone, ;
DISPOSE;
END;