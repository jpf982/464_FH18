

module Bands
using UsefulFunctions
#using Arpack
using LinearAlgebra

export getBands, project

function interpolate(n,klist,a)
	kdict = Dict(
		    "Γ" => [0;   0;   0],
		    "K" => [1/2; tand(30)/2; 0],
		    "M" => [1/2; 0;   0],
		    "M-" => [-1/2; 0;   0],
		    "A" => [0;   0; 1/2],	
		    "H" => [1/3;1/3;1/2]
		    )	    
	#highSym = map(k->kdict[k], klist)
	highSym = (4*π/a)*map(k->kdict[k], klist)
	kpts = Any[]
	d = 1/n
	for k1 in 1:(size(highSym)[1]-1)
		k2 = k1 + 1
		for f = 0:d:(1-d) #fraction of the 2nd kpt
			k = (1-f)*highSym[k1] + f*highSym[k2]
			push!(kpts,k)
		end
	end
	push!(kpts,highSym[end])
	return kpts
end

function getBands(klist, n, a, Hofk) #takes in array of kpt strings, number of interpolation pts, H(k) function
	kpts = interpolate(n,klist,a)
	testH = Hofk([0;0;0])
	#initialize the band array
	λ_test, evecs_test = eigen(testH)
	#λ_test, evecs_test = eig(testH, 1E-12)
	nk = size(kpts)[1]
	nE = size(λ_test)[1]
	ndim = size(evecs_test)[2]
	Evals = zeros(Float64, nk, nE)
	Estates = zeros(ComplexF64, nk, nE, ndim) 
	#go through and fill it up
	
	#
	nEig = size(testH)[1]
	if(nE < size(testH)[1])
		println("Warning! $nE / $nEig eigvls are being calculated\n")
	end
	#d = 100
	for ik in 1:nk
		k = kpts[ik]
		H = Hofk(k)
		#Eofk, Estatek = eigs(Hermitian(H))
		#Eofk, Estatek = eigen(H)
		#Eofk, Estatek = eigen(Hermitian(H))
		Eofk, Estatek = eig(H,1E-12)
		#Eofk = eigvals(H)
		for iE in 1:nE
			Evals[ik,iE] = real(Eofk[iE]) 
		end
		#Estatesk = eigvecs(H)
		for iE1 in 1:nEig; for iE2 in 1:nEig
				Estates[ik,iE1,iE2] = Estatek[iE1,iE2]
			end
		end
	end
	return Evals, Estates
end

function project(projKet, Estates) #takes in array of kpt strings, number of interpolation pts, H(k) function
	nk = size(Estates)[1]
	nE = size(Estates)[2]
	projVals = zeros(Float64, nk, nE)
	adjoint = projKet' #takes |proj> -> <proj|
	for ik in 1:nk
		for iE in 1:nE
			projVals[ik,iE] = abs(adjoint*Estates[ik,iE,:])^2 #performs <proj|band>
		end
	end
	return projVals
end


#function plotBands(klist, n, E)
#	nk = length(klist)
#	indices = LinRange(0,nk,nk*n+1) 
#	
#
#end

end
