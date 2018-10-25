function [frame] = warping(inVert,newVert,Triangles,Img)
%warping Find the Affine Transform Parameters of given vertices
%   inVert, newVert: num_vert x 2
%   Triangles: num_tri x 2
%   Return a deformed Img
%% Get Triangle Vertices
center_lambda=[1/3;1/3;1/3];
nt = size(Triangles,1);
old_coords = zeros(2,3,nt);
new_coords = zeros(2,3,nt);
%new_center=zeros(2,nt);
for t=1:nt
    v = Triangles(t,:);
    old_coords(:,:,t) = inVert(v,:)';
    new_coords(:,:,t) = newVert(v,:)';
    %new_center(:,t)=newVert(v,:)'*center_lambda;
    
end


%% Deform Img using Reverse Mapping
frame = zeros(size(Img));
CT = zeros(size(Img));
for x = 1:size(Img,2)
    for y = 1:size(Img,1)
        % Find Triangle and lambda
        
        tri = 0;
        for t=1:nt
            temp = [new_coords(:,:,t);ones(1,3)]\[x,y,1]';
            if all(temp>=0) && all(temp<=1)
                lambda = temp;
                tri = t;
                break
            end
        end
        CT(y,x) = tri;
        if tri==0
            continue
        end
        %{
        
        distance=sum((new_center-nt).^2);
        [~,rank]=sort(distance);
        tri = 0;
        for t=1:nt
            temp = [new_coords(:,:,rank(t));ones(1,3)]\[x,y,1]';
            if all(temp>=0) && all(temp<=1)
                lambda = temp;
                tri = rank(t);
                break
            end
        end
        CT(y,x) = tri;
        if tri==0
            continue
        end
        %}
        
        % Find (u,v)
        point = [old_coords(:,:,tri);ones(1,3)]*lambda;
        u = point(1);
        v = point(2);
        % Bilinear Interpolation
        u1 = floor(u);
        u2 = ceil(u);
        v1 = floor(v);
        v2 = ceil(v);
        if u1==0
            u1=1;
        end
        if v1==0
            v1=1;
        end
        if v2==80
            v2=79;
        end
        if u2==131
            u2=130;
        end
        if u1~=u2
            a = interp1([u1,u2],[Img(v1,u1),Img(v1,u2)],u);
            b = interp1([u1,u2],[Img(v2,u1),Img(v2,u2)],u);
        else
            a = Img(v1,u1);
            b = Img(v2,u1);
        end
        if v1~=v2
            frame(y,x) = interp1([v1,v2],[a,b],v);
        else
            frame(y,x) = a;
        end
    end
end
end

