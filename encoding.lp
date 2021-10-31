% encoding for placing as much rectangles as possible into a bigger rectangle

% calculate possible (mathematical) number of rectangles which can be packed into 
max_rects(N) :- N = (Width*Height) / (W*H), rect_dim(W,H), big_rectangle(Width, Height).

% a rectangles are allowed to rotate
{r(1,W,H);r(1,H,W)} 1 :- rect_dim(W,H).
{r(I+1,W,H);r(I+1,H,W)} 1 :- r(I,W,H), max_rects(Max), I <= Max. 

% encoding inspired by https://arxiv.org/pdf/1705.04569.pdf

&dom{0..Width-W} = x(I) :- r(I,W,H), big_rectangle(Width,_).
&dom{0..Height-H} = y(I) :- r(I,W,H), big_rectangle(_,Height).

% at least one relations must hold so that n two rectangles overlap
1 { le(x(I),WI,x(J));
    le(x(J),WJ,x(I));
    le(y(I),HI,y(J));
    le(y(J),HJ,y(I)) } :- r(I,WI,HI), r(J,WJ,HJ), I < J.

&sum{VI; C} <= VJ :- le(VI,C,VJ).

% maximize num of rectangles and minimize rotated ones
#maximize{1@10,I:r(I,_,_)}.
#minimize{1@5,I:r(I,H,W), rect_dim(W,H)}.


% show statements
#show r/3.
#show max_rects/1.
#show is_rotated(I) : r(I,H,W), rect_dim(W,H).
#show big_rectangle/2.

&show {x/1}.
&show {y/1}.
