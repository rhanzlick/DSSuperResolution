%Adaptation of Diamond Square Algorithm for Image Upscaling
%Author: Ryan Hanzlick
%Date: 05-27-19
clear
close
clc

tic
iterations = 1;             %Number of times resolution of each dimension will be increased by 2x-1
imageSteps=cell(1,iterations);
originalImg = imread('img1.png');
%originalImg = imread('AlexandRyan.jpg');
img=originalImg;
%img = rgb2gray(img);
rgb = length(img(1,1,:));   %number of color channels to consider
res = size(img);            %resolution of initial image

%Enlarge initial image by inserting zero rows/columns
imgCell = cell(1,rgb);
newImg = cell(1,rgb);

for iter=1:iterations
    
if(iter>1)
    img=finalImg;
    res = size(img);            %resolution of initial image
end
    
    for layers=1:rgb
        imgCell{layers}=img(:,:,layers);
        newImg{layers} = zeros((2*res(1))-1,(2*res(2)-1));
    end


    for z = 1:rgb
%%
    flag=0;
%Enlarge
        for i=1:res(1)
            for j=1:res(2)
                newImg{z}(2*i-1,2*j-1)=img(i,j,z);     %increase each dimension by (2x-1)
            end
        end

        newRes = size(newImg{z});
    

%%
%Pad matrix for diamond-square process
        newImg{z} = [zeros(newRes(1),1),newImg{z},zeros(newRes(1),1)];
        newImg{z} = [zeros(1,newRes(2)+2);newImg{z};zeros(1,newRes(2)+2)];

        newRes = size(newImg{z});


%%
%Calculate Square centers
        for i=3:2:newRes(1)-2
            if(i/(newRes(1)-2)>0.5&&flag==0)
                disp(cat(2,'Square 50% complete for color ',num2str(z),'. Elapsed Time: ',num2str(toc)))
                flag=1;
            end
            for j=3:2:newRes(2)-2
                newImg{z}(i,j) = 0.25*(newImg{z}(i+1,j-1)+newImg{z}(i+1,j+1)+newImg{z}(i-1,j-1)+newImg{z}(i-1,j+1));
            end
        end


%%
%Calculate Diamond centers

%newHeight = length(newImg(:,1));
%newWidth = length(newImg(1,:));

        for i=2:1:newRes(1)-1
            if(i/(newRes(1)-1)==0.5)
                disp(cat(2,'Diamond 50% complete for color ',num2str(z),'. Elapsed Time: ',num2str(toc)))
            end
            for j=3-mod(i,2):2:newRes(2)-1
                newImg{z}(i,j) = 0.25*(newImg{z}(i-1,j)+newImg{z}(i+1,j)+newImg{z}(i,j-1)+newImg{z}(i,j+1));
            end
        end


%%
% Renormalize enlarged image values
        newImg{z}=newImg{z}/max(newImg{z}(:));
% Remove Padding
        newImg{z}(newRes(1),:)=[];newImg{z}(1,:)=[];newImg{z}(:,newRes(2))=[];newImg{z}(:,1)=[];

    end

%%
%Concat each color
    finalImg = cat(3,newImg{:});
%Store iteration
    imageSteps{iter}=finalImg;
end

%Compare to standard methods including:
%ALinear = imresize(originalImg,[1313 1999],'bilinear');

%%
%{
%*OPTIONAL* post-process filtering
hp=[0,-1,0;-1,5,-1;0,-1,0]; %highpass filter kernel
lp1=(1/16)*[1,2,1;2,5,2;1,2,1]; %lowpass filter kernel
lp2=ones(3)/9; %low pass filter kernel

for fLayers = 1:rgb
    finalImg(:,:,fLayers)=imfilter(finalImg(:,:,fLayers),lp2);    %apply low pass filter - remove noise
    finalImg(:,:,fLayers)=imfilter(finalImg(:,:,fLayers),hp);     %apply high pass filter - sharpen image details
    finalImg(:,:,fLayers)=medfilt2(finalImg(:,:,fLayers));        %apply median filter - remove any salt and pepper noise
end

%%Weiner Filter
%finalImg=deconvwnr(finalImg,[1,.01],0);
imwrite(finalImg,'C:\Users\Ryan\Desktop\Code_Projects\Image_Upscaling\GrafeBridalPartyGuys-84_sharp1.png')
%}
%***********************





%Output initial and final images for comparison


imshow(originalImg)
title('Original Image')
figure
imshow(finalImg)  %output new image
title('Enlarged Image')


toc
