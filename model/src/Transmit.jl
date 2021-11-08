module Transmit

using LinearAlgebra
#using GenericLinearAlgebra
using UsefulFunctions
using Arpack
using Constants

export transmission

function transmission(pwSolver,Nlayers,ω_begin,ω_end,nω=100)
	Tvals = zeros(nω);
	ωvals = LinRange(ω_begin,ω_end,nω);
	iR = 2*Nlayers - 1 # index transmitted light in vector
	n = 1
	for ω in ωvals
		A, b = pwSolver(ω)
		#println("\nCondition number = ")
		#show(cond(A))
		x = A \ b
		#x = (A' * A) \ (A' * b)
		#=show(A)
		println("\n")
		println("\n")
		show(x)
		println("\n") =#
		T = abs(x[iR])^2
		if(ω == 0.0)
			Tvals[n] == 1
		else
			Tvals[n] = T
		end
		n += 1
	end
	return Tvals, (1/THz)*ωvals
end
end
