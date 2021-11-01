% encoding for placing as much rectangles as possible into a bigger rectangle

min_side_length(Min) :- Min = #min{W: rect_dim(W,_); H: rect_dim(_,H)}.
num_rects_per_width(X) :- big_rectangle(Width,_), min_side_length(Min), X=(Width/Min)+1.  % division can be smarter and +1 can be saved sometimes

% calculate possible (mathematical) number of rectangles which can be packed into 
max_rects(N) :- N = (Width*Height) / (W*H), rect_dim(W,H), big_rectangle(Width, Height).

% a rectangles are allowed to rotate by 90° (270°)
{r(1,W,H);r(1,H,W)} 1 :- rect_dim(W,H).
{r(I+1,W,H);r(I+1,H,W)} 1 :- r(I,_,_), rect_dim(W,H), max_rects(Max), I+1 <= Max. 

% encoding inspired by https://arxiv.org/pdf/1705.04569.pdf

&dom{0..Width-Min} = x(I) :- I=1..Max, max_rects(Max), min_side_length(Min), big_rectangle(Width,_).
&dom{0..Height-Min} = y(I) :- I=1..Max, max_rects(Max), min_side_length(Min), big_rectangle(_,Height).


% at least one relations must hold so that not two rectangles overlap
1 { le(x(I),WI,x(J));
    le(x(J),WJ,x(I));
    le(y(I),HI,y(J)) } 1 :- r(I,WI,HI), r(J,WJ,HJ), I < J, I+NP+1>=J, num_rects_per_width(NP).

&sum{VI; C} <= VJ :- le(VI,C,VJ).

&sum{x(I)} <= Width-W :- r(I,W,H), big_rectangle(Width,_). 
&sum{y(I)} <= Height-H :- r(I,W,H), big_rectangle(_,Height). 

% maximize number of rectangles and not rotated ones
#maximize{1,I:r(I,_,_);1,I,straight:r(I,W,H), rect_dim(W,H)}.

%%% symmetry breaking stuff
:- r(I,_,_), r(I+1,_,_), &sum{x(I)} > x(I+1). % order by x position
:- r(I,_,_), r(I+1,_,_), &sum{x(I)} = x(I+1), &sum{y(I)} > y(I+1). % order by y position
:- r(I,H,W), r(I+1,W,H), &sum{x(I)} = x(I+1), &sum{y(I)} = y(I+1), rect_dim(W,H). % order by rotation

&sum{x(I)} = 0 :- not r(I,_,_), max_rects(Max), I=1..Max. % default for unchosen boxen
&sum{y(I)} = 0 :- not r(I,_,_), max_rects(Max), I=1..Max. % default for unchosen boxen


% show statements
#show r/3.
#show max_rects/1.
#show is_rotated(I) : r(I,H,W), rect_dim(W,H), not W==H.
#show big_rectangle/2.

&show {x/1}.
&show {y/1}.
