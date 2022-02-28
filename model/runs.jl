push!(LOAD_PATH, "./")
push!(LOAD_PATH, "./src/")

using thinfilm
using Printf
using Random
using Distributions
using PlotStuff
using UsefulFunctions
using Constants
using Random

function mkfolder(path)
	if(isdir(path))
		println("$path already exists...")
		#rm(path, recursive=true)
	else
		mkdir(path)
	end
end
	
Air  = 		Layer("Air",     	1, 1, 0.5*10^6*nm,		0);
Substrate=	Layer("Glass",  	5, 1,10^6*nm,    	0);

function genGaussianRandomStack(n) # this is arbitrary and ugly for now, do  not worry
	#param of layer:name, εᵣ  μᵣ  Δx (nm), σ (S/m)
	PhQ = []
	dx1 = Normal(40,2)
	dx2 = Normal(200,10)
	for i = 1:n
		#dx1 = 80*rand(); dx2 = 400*rand();
		Si 	=     	Layer("Si",	  11.9, 1, rand(dx1)*nm, 10^(-3));
		Glass	=   	Layer("SiO2",    5, 	1, rand(dx2)*nm, 10^(-11));
		PhQ = vcat(PhQ,Glass,Si)
	end
	return PhQ
end

function genRandomStack(n) # this is arbitrary and ugly for now, do  not worry
	#param of layer:name, εᵣ  μᵣ  Δx (nm), σ (S/m)
	PhQ = []
	for i = 1:n
		dx1 = 80*rand(); dx2 = 400*rand();
		Si 	=     	Layer("Si",	  11.9, 1, dx1*nm, 10^(-3));
		Glass	=   	Layer("SiO2",    5, 	1, dx2*nm, 10^(-11));
		PhQ = vcat(PhQ,Glass,Si)
	end
	return PhQ
end

function addAir(stack)
	return vcat(Air,stack,Air)
end

function Translate(stack, air=true)
	Nlayers = size(stack)[1]  # get rid of the two air layers
	if(air)
		Tstack = copy(stack)
		poppedLayer = splice!(stack,2)
		#insert!(stack,)
		insert!(Tstack, Nlayers - 1, poppedLayer)
	end
	return Tstack
end

function genPhCStack(n) # this is arbitrary and ugly for now, do  not worry
	#param of layer:name, εᵣ  μᵣ  Δx (nm), σ (S/m)
	Air  = 	  Layer("Air",     1, 1, 800*nm,		0);
	Substrate=Layer("Substrate",  5, 1,10^6*nm,    	0);
	dx1 = 200*rand(); dx2 = 250*rand()
	Si1 =     Layer("Si", 11.9, 1, dx1*nm,		0);
	Glass1=   Layer( "SiO2",   5, 1, dx2*nm,	   	0);
	dx1 = 300*rand(); dx2 = 300*rand() 
	Si2 =     Layer("Si", 11.9, 1, dx1*nm,	     	0);
	Glass2=   Layer("SiO2",    5, 1, dx2*nm,	   	0);
	PhC₁ = []
	PhC₂ = []
	for i = 1:n
		PhC₁ = vcat(PhC₁,Si1,Glass1)
		PhC₂ = vcat(PhC₂,Si2,Glass2)
	end
	TPhQ = vcat(PhC₁,PhC₂)
	#Chip = vcat(Air,TPhQ,Substrate,Air)
	return TPhQ
end

function TwoStageSpectra(n,nω,dzmin,dzmax,ndz,smoothing)
	toppath = "./testing/twostage"
	mkfolder(toppath)
	baseChip = genRandomStack(n)
	baseChip2 = genRandomStack(n)
	#dzmax = 0.05; dzmin = 0.0; dz = 0.003
	ΔzVals = collect(LinRange(dzmin,dzmax,ndz))
	spectra = zeros(size(ΔzVals)[1],nω)
	for i in eachindex(ΔzVals) # spacing in mm 
		Δz = ΔzVals[i]
		name="dz_$Δz-mm"	
		path = toppath*"/2stage-"*name
		mkfolder(path)
		spacer  =  Layer("Air", 1, 1, Δz*10^6*nm,0);
		chip = addAir(vcat(baseChip,spacer,baseChip2))
		T = main(chip,path,name,nω,smoothing)
		spectra[i,:] = T
		#show(spectra)
		chip = Translate(chip)
	end
	#plotSurf(collect(LinRange(0,1000,nω)),ΔzVals,spectra',"w (THz)","Spacer Thickness (mm)")
	#imshow(z,cmap="cividis")
	plot2D(spectra',dzmin,dzmax,0,1000,"Spacer Thickness (mm)","ω (THz)")
end

function offsetSpectra(nChips,n,nω,smoothing)
	toppath = "./testing/gaussianOffset"
	mkfolder(toppath)
	spectra = zeros(nChips,nω)
	for m = 1:nChips
		#chip = vcat(Air,genPhCStack(n),Substrate,Air)
		chip = vcat(Air,genGaussianRandomStack(n),Substrate,Air)
		name="T_$m"	
		path = toppath*"/random-"*name
		mkfolder(path)
		T = main(chip,path,name,nω,smoothing)
		#avgspectra = main(chip,path,name,nω,smoothing,θ₁,θ₂,nθ)
		#spectra[m,:] = avgspectra[1,:]
		spectra[m,:] = T
	end
	for i = 1:nChips
		for j = (i+1):nChips
			println("m(T$i,T$j) = $(Rmetric(spectra[i,:],spectra[j,:]))")
		end
	end
end

function TranslationSpectra(n,nω,smoothing)
	toppath = "./testing/permute"
	mkfolder(toppath)
	baseChip = addAir(genRandomStack(n))
	chip = baseChip
	spectra = zeros(n,nω)
	np = 5
	for m = 1:np
		name="T_$m"	
		path = toppath*"/permute-"*name
		mkfolder(path)
		T = main(chip,path,name,nω,smoothing)
		spectra[m,:] = T
		#show(spectra)
		chip = Translate(chip)
	end
	for i = 1:np
		for j = (i+1):np
			println("m(T$i,T$j) = $(Rmetric(spectra[i,:],spectra[j,:]))")
		end
	end
end

function RandomChips(n,nChips,nω,smoothing)
	toppath = "./testing/angle"
	mkfolder(toppath)
	for m = 1:nChips
		chip = addAir(genRandomStack(n))
		spectra = zeros(n,nω)
		name="T_$m"	
		path = toppath*"/random-"*name
		mkfolder(path)
		T = main(chip,path,name,nω,smoothing)
		spectra[m,:] = T
	end
end


nω = 4000; smoothing = 15; nChips = 5; n = 3
θ₁ = 0; θ₂ = 20; 
nθ = 60; 
#TwoStageSpectra(15,nω,0.0,0.06,601,smoothing)
#RandomChips(3,nChips,nω,smoothing)

offsetSpectra(nChips,n,nω,smoothing)

#=toppath = "./testing/kktest"
mkfolder(toppath)
for m = 1:nChips
	#chip = vcat(Air,genPhCStack(n),Substrate,Air)
	chip = vcat(Air,genRandomStack(n),Substrate,Air)
	name="T_$m"	
	path = toppath*"/random-"*name
	mkfolder(path)
	main(chip,path,name,nω,smoothing,θ₁,θ₂,nθ)
end=#

#=toppath = "./testing"
mkfolder(toppath)

for i in 1:5
	
	name="test$i"	
	path = toppath*"/example-"*name
	mkfolder(path)
	chip = genRandomStack()
	main(chip,path,name,nω,smoothing)
	
	#path = toppath*"/example-rev"*name
	#mkfolder(path)
	#main(reverse(chip),path,name,nω,smoothing)
end
=#
	#save = true
#rm(toppath, recursive=true)
#σ1 = 0.5*nm; σ2 = 3.5*nm; dσ = 1*nm
#h0 = 1*m; h2 = 5*nm; dh = 1*nm
#for fᵤ = 0.6:0.2:1
	#path = toppath*"/"*(@sprintf("L#%i_S#%g_dh0#%g_fu#%g_theta#%g_U#%g_mu#%g_V0#%g_U2#%g",λ,σ,Δh0,fᵤ,θ,U,μ,V₀,U₂))
	#mkdir(path)
	#for σ = σ1:1*nm:σ2
	#main(λ, σ, Δh0, fᵤ, U, μ, V₀, U₂, θ, save,path)
	#end
#end



