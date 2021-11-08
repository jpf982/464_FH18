push!(LOAD_PATH, "./")
push!(LOAD_PATH, "./src/")

using thinfilm
using Printf
using Random
using PlotStuff
using UsefulFunctions
using Constants

function mkfolder(path)
	if(isdir(path))
		println("$path already exists...")
		#rm(path, recursive=true)
	else
		mkdir(path)
	end
end
	
Air  = 		Layer("Air",     	1, 1, 0.5*10^6*nm,		0);
Substrate=	Layer("Substrate",  	5, 1,10^6*nm,    	0);

function genRandomStack(n) # this is arbitrary and ugly for now, do  not worry
	#param of layer:name, εᵣ  μᵣ  Δx (nm), σ (S/m)
	PhQ = []
	for i = 1:n
		dx1 = 150*rand(); dx2 = 150*rand();
		Si 	=     	Layer("Si",	  11.9, 1, dx1*nm,	0);
		Glass	=   	Layer("Glass",    5, 	1, dx2*nm,	0);
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

function genPhCStack() # this is arbitrary and ugly for now, do  not worry
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
	for i = 1:6
		PhC₁ = vcat(PhC₁,Si1,Glass1)
		PhC₂ = vcat(PhC₂,Si2,Glass2)
	end
	TPhQ = vcat(PhC₁,PhC₂)
	Chip = vcat(Air,TPhQ,Substrate,Air)
	return Chip
end

function TwoStageSpectra(n,nω,smoothing)
	toppath = "./testing/twostage"
	mkfolder(toppath)
	baseChip = genRandomStack(n)
	baseChip2 = genRandomStack(n)
	spectra = zeros(n,nω)
	for Δz = 0:0.1:0.5 # spacing in mm 
		name="dz_$Δz-mm"	
		path = toppath*"/2stage-"*name
		mkfolder(path)
		spacer  =  Layer("Air", 1, 1, Δz*10^6*nm,0);
		chip = addAir(vcat(baseChip,spacer,baseChip2))
		T = main(chip,path,name,nω,smoothing)
		spectra[m,:] = T
		#show(spectra)
		chip = Translate(chip)
	end
	heatmap(spectra)
end

function TranslationSpectra(n,nω,smoothing)
	toppath = "./testing/permute"
	mkfolder(toppath)
	baseChip = addAir(genRandomStack(n))
	chip = baseChip
	spectra = zeros(n,nω)
	np = 10
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
nω = 2*10^3; smoothing = 10


TranslationSpectra(10,nω,smoothing)
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



