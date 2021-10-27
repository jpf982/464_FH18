
module UsefulFunctions

using LinearAlgebra

export ⊗,⋅,×

⊗(A,B) = kron(A,B)
×(u,v) = cross(u,v)

function rotate(θ::Float64)
	return [cos(θ) -sin(θ) 0; sin(θ) cos(θ) 0; 0 0 1]
end


function mean(v)
        N = size(v)[1]
        sum = 0
        for i in v
                sum += i
        end
        return sum/N
end

movingaverage(g, n) = [i < n ? mean(g[begin:i]) : mean(g[i-n+1:i]) for i in 1:length(g)]

function eig(A, conv)
	nA = size(A)[1]
	n = nA # num of eigvls to calculate
	λ = zeros(Float64,n)
	d = 100 # value added to diagonal to make all eigvls positive
	vecs = zeros(ComplexF64,n,n)
	M = zeros(ComplexF64,nA,nA)
	M .= A + d*I(nA)
	for i in 1:n
		#get initial random vectors
		v = rand(ComplexF64,n)
		v .= v/norm(v)
		v_prior = rand(ComplexF64,n)

		#will find the largest eigenvector/eigvl of M
		error = 100
		#println("eigvl # $i")
		#println("\n Eigvl #$i")
		#j = 0
		#for Ω = 1:10000
		while(error > conv)
			v .= M*v
			#println("error = $error")
			error = abs(1 - norm(v)/norm(v_prior)) #works off eigenvalue convergence, instead of eigvec convergence
			v_prior .= v
			#display(v)
			v .= v/norm(v)
			#j += 1
		end
		E = norm(M*v)

		#subtract off contribution of Eₙ
		M .-=  E*v*v'

		#write into output 
		λ[i] = E - d
		for j in 1:n
			vecs[i,j] = v[j]
		end
		#println("norm(A - PDP†) = \n")
		#display(norm(A .-vecs'*Diagonal(λ)*vecs))
		#println("")
	end
	return λ, vecs
end

for n in names(@__MODULE__; all=true)
               if Base.isidentifier(n) && n ∉ (Symbol(@__MODULE__), :eval, :include)
                   @eval export $n
               end
       end

end
