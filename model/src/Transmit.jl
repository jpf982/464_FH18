module Transmit

using LinearAlgebra
#using GenericLinearAlgebra
using UsefulFunctions
using Arpack
using Constants

export transmission

function transmission(pwSolver,Nlayers,ω_begin,ω_end,nω=100,θ₀=0)
	Tvals = zeros(nω);
	ωvals = LinRange(ω_begin,ω_end,nω);
	iR = 2*Nlayers - 1 # index transmitted light in vector
	n = 1
	for ω in ωvals
		A, b = pwSolver(ω,θ₀)
		#println("\nCondition number = ")
		#show(cond(A))
		try
			x = A \ b
			T = abs(x[iR])^2
			if(isnan(T))
				Tvals[n] == 1
			else
				Tvals[n] = T
			end
		catch
			Tvals[n] = 0
		end
		n += 1
	end
	return Tvals, (1/THz)*ωvals
end
end
