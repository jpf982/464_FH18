

module ConstructHamiltonian
#push!(LOAD_PATH, "./src/")
using LinearAlgebra
#using SparseArrays
using Operators
using UsefulFunctions
using Constants

export pwCoeffs


#=function phaseAtInterface(layers,k₀)
	nLayers = size(layers)[1];
	ΦvsX = zeros(nLayers);
	ΦatX = 0;
	ΔΦ = 0
	for i = 1:nLayers
		ΦvsX[i] = ΦatX + ΔΦ;
		ΔΦ = √(layers[i].εᵣ*1)*k₀*layers[i].Δx;	
	end
	return ΦvsX;
end =#


struct PW
	i::Int #layer index of corresponding PWs
	γ # goes in eq exp(γ⋅R)
	η # intrinsic impedance
	edgeL
	edgeR
end



function pwCoeffs(layers, wrap=false)
	Nlayers = size(layers)[1];
	N = 2*Nlayers
	
	PWs = PW[]
	n = 1 #PW num
	xL = 0 #left edge of particular layer
	xR = 0 #right edge
	for L in layers
		xR += L.Δx
		#γ = ω -> abs(ω)*√(L.μᵣ*μ₀*L.εᵣ*ε₀)
		#η = ω -> √((L.μᵣ*μ₀)/(L.εᵣ*ε₀)) 
		γ = ω -> √(im*ω*L.μᵣ*μ₀*(L.σ + im*ω*L.εᵣ*ε₀)) 
		η = ω -> √(im*ω*L.μᵣ*μ₀/(L.σ + im*ω*L.εᵣ*ε₀)) 
		PWlayer = PW(n,γ,η,xL,xR)
		xL += L.Δx
		push!(PWs,PWlayer)
		n += 1
	end
	
	
	function pwSolver(ω)
		# set up Ax = b
		# x = array of PW coefficients for [each layer] ⊗ [left, right movers]
		
		# we will consider the "first" interface at x = 0.
		# initialize beginning right-moving wave amplitude = 1
		#A[1,1] = 1; b[1] = 1
		if(wrap == false)
			A = zeros(ComplexF64,N,N) #generate matrix of coefficients to give to H(k)
			#A = zeros(Complex{BigFloat},N,N) #generate matrix of coefficients to give to H(k)
			b = zeros(N)
			# if periodic boundaries are off, we will do a trick and
			#initialize end left-moving wave = 0 if no PBC
			A[1,1] = 1; b[1] = 1
			A[2,N] = 1; b[2] = 0

			# we will also over-fit the matrix so that it becomes less ill-conditioned
			# we know 1 + R = T; R - T = 1
			#b[N+1] = 1; A[N+1,2] = 1; A[N+1,N-1] = -1
		else
			A = zeros(ComplexF64,N,N) #generate matrix of coefficients to give to H(k)
			b = zeros(N)
			# set E₁ = E₂ = A + B = Y + Z; A + B - Y - Z = 0
			A[1,1] = 1; b[1] = 1
			A[2,1] = 1; A[2,2] = 1; A[2,N] = -1; A[2,N-1] = -1;
		end
		
		# loop over remaining interfaces
		for i = 2:Nlayers
			#the two layers around an interface:
			L1 = PWs[i-1]; L2 = PWs[i]
			# first solve Eᵢ = Eᵢ₊₁
			iE = 2*i - 1 # row to insert in matrix
			A[iE,2*i-3] = exp(L1.γ(ω)*L1.edgeR); 
			A[iE,2*i-2] = exp(-L1.γ(ω)*L1.edgeR);
			A[iE,2*i-1] = -exp(L2.γ(ω)*L2.edgeL);
			A[iE,2*i]   = -exp(-L2.γ(ω)*L2.edgeL);
		
			#then solve Hᵢ = -Hᵢ₊₁
			iH = 2*i
			A[iH,2*i-3] = exp(L1.γ(ω)*L1.edgeR)/L1.η(ω); 
			A[iH,2*i-2] = -exp(-L1.γ(ω)*L1.edgeR)/L1.η(ω);
			A[iH,2*i-1] = -exp(L2.γ(ω)*L2.edgeL)/L2.η(ω);
			A[iH,2*i]   = exp(-L2.γ(ω)*L2.edgeL)/L2.η(ω);
		end
		#A .+= 10^-12*Diagonal(ones(N))
		return A, b
	end
	return pwSolver
end
end