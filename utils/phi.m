function phi_out = phi(u,v)

sigma = 1;
% phi_out = exp(-(1/(2*sigma^2))*(repmat(sqrt(sum(u.^2,2).^2),1,size(v,1))...
%              -2*(u*v')+repmat(sqrt(sum(v.^2,2)'.^2),size(u,1),1)));
phi_out = -pdist2(u,v);
end

