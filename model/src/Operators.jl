
module Operators

using LinearAlgebra
using Constants

σ₀ = [
      1 0
      0 1
     ]

σ₁ = [
      0  1 
      1  0
     ] 
σ₂ = [
      0 -im 
      im  0
     ] 
σ₃ = [
      1  0
      0 -1
     ]

S₁ = (1/2)*ħ*σ₁; S₂= (1/2)*ħ*σ₂; S₃ = (1/2)*ħ*σ₃; 
S = cat(S₁,S₂,S₃, dims = 3);
#σ = Array[σ₁;σ₂;σ₃];
x₊ = √(1/2)*[1;1]; x₋ = √(1/2)*[1;-1]; 
y₊ = √(1/2)*[1;im]; y₋ = √(1/2)*[1;-im]; 
z₊ = [1;0]; z₋ = [0;1];

#μ = μB * σ

Hₙ = Diagonal([-Ry*q^2/n^2 for n = 1:6])


function L₃(l) 
	return Diagonal([ħ*m for m = -l:l])
end


for n in names(@__MODULE__; all=true)
               if Base.isidentifier(n) && n ∉ (Symbol(@__MODULE__), :eval, :include)
                   @eval export $n
               end
end

end
