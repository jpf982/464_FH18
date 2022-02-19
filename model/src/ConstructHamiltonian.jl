

module ConstructHamiltonian
#push!(LOAD_PATH, "./src/")
using LinearAlgebra
#using SparseArrays
using Operators
using UsefulFunctions
using Constants
using Dielectric

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
	i #layer index of corresponding PWs
	γ # goes in eq exp(γ⋅R)
	η # intrinsic impedance
	edgeL
	edgeR
	n # refractive index
	kzᵢ # angle of light in layer
end


function pwCoeffs(layers, wrap=false)
	Nlayers = size(layers)[1];
	N = 2*Nlayers
	
	PWs = PW[]
	i = 1 #PW num
	xL = 0 #left edge of particular layer
	xR = 0 #right edge
	for L in layers
		xR += L.Δx
		εᵣ = ε_mat(L.name)
		γ = ω -> √(im*ω*L.μᵣ*μ₀*(im*ω*εᵣ(ω)*ε₀)) 
		#γ = ω -> √(im*ω*L.μᵣ*μ₀*(im*ω*εᵣ(ω)*ε₀)) 
		#η = ω -> √(im*ω*L.μᵣ*μ₀/(im*ω*εᵣ(ω)*ε₀)) 
		n = ω -> √(εᵣ(ω)*L.μᵣ)
		η = ω -> η₀/n(ω)
		#n = ω -> η₀/η(ω)
		kzᵢ(kx₀,kz₀,ω) = √(kz₀^2 + (1/n(ω)^2 - 1)*kx₀^2)
		#kzᵢ(kx₀,kz₀,ω) = (1/n(ω))*√( kz₀^2 + (1-n(ω)^2)*kx₀^2 )
		PWlayer = PW(i,γ,η,xL,xR,n,kzᵢ)
		xL += L.Δx
		push!(PWs,PWlayer)
		i += 1
	end
	
	function pwSolver(ω, θ₀=0)
		# set up Ax = b
		# x = array of PW coefficients for [each layer] ⊗ [left, right movers]
		
		# we will consider the "first" interface at x = 0.
		# initialize beginning right-moving wave amplitude = 1
		#A[1,1] = 1; b[1] = 1
		k₀ = ω/c
		kx₀ = sin(θ₀)*k₀
		kz₀ = cos(θ₀)*k₀
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
			
			# generate wavenumbers in layer i-1, i
			kz₁ = L1.kzᵢ(kx₀,kz₀,ω); kz₂ = L2.kzᵢ(kx₀,kz₀,ω);

			# first solve Eᵢ = Eᵢ₊₁
			iE = 2*i - 1 # row to insert in matrix
			A[iE,2*i-3] =  exp(im* kz₁*L1.edgeR); 
			A[iE,2*i-2] =  exp(im*-kz₁*L1.edgeR);
			A[iE,2*i-1] = -exp(im* kz₂*L2.edgeL);
			A[iE,2*i]   = -exp(im*-kz₂*L2.edgeL);
		
			#then solve Hᵢ = -Hᵢ₊₁
			iH = 2*i
			A[iH,2*i-3] =  exp(im* kz₁*L1.edgeR)/L1.η(ω); 
			A[iH,2*i-2] = -exp(im*-kz₁*L1.edgeR)/L1.η(ω);
			A[iH,2*i-1] = -exp(im* kz₂*L2.edgeL)/L2.η(ω);
			A[iH,2*i]   =  exp(im*-kz₂*L2.edgeL)/L2.η(ω);
		end
		#A .+= 10^-12*Diagonal(ones(N))
		return A, b
	end
	return pwSolver
end
end
