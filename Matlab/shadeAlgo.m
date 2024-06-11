%clear
%clc
%A=imread('img2.png');
B=A;
for i=1:length(A(:,1,1))
    tic
if(i==0.01*length(A(:,1,1)))
disp('1% Complete')
toc
end
if(i==0.25*length(A(:,1,1)))
disp('25% Complete')
toc
end
if(i==0.5*length(A(:,1,1)))
disp('50% Complete')
toc
end
if(i==0.75*length(A(:,1,1)))
disp('75% Complete')
toc
end
for j=1:length(A(1,:,1))
if(j==2)
end
if(A(i,j,1)>=0.95*max(A(:))||A(i,j,2)>=0.95*max(A(:))||A(i,j,3)>=0.95*max(A(:)))

%B(i,j,1)=.9*A(i,j,1);
%B(i,j,2)=.9*A(i,j,2);
%B(i,j,3)=.9*A(i,j,3);
%B(i,j,1)=(A(i,j,1)/max(A(:)))*A(i,j,1);
%B(i,j,2)=(A(i,j,2)/max(A(:)))*A(i,j,2);
%B(i,j,3)=(A(i,j,3)/max(A(:)))*A(i,j,3);
%B(i,j,:)=0.6*A(i,j,:);
end
end
end
disp('100% Complete')
A=B;
figure
imshow(B)
%imshow(A)
%figure
%imshow(B)