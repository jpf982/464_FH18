push!(LOAD_PATH, "./")
push!(LOAD_PATH, "./src/")

using thinfilm
using Printf
using Random
using Constants

function mkfolder(path)
	if(isdir(path))
		println("$path already exists...")
		#rm(path, recursive=true)
	else
		mkdir(path)
	end
end

function genRandomStack() # this is arbitrary and ugly for now, do  not worry
	Air  = Layer(     1, 1, 800*nm,		0);
	Substrate=Layer(  5, 1,10^6*nm,    	0);
	dx1 = 100*rand(1)[1] + 50; dx2 = 150*rand(1)[1] + 50
	Si1 =   Layer( 11.9, 1, dx1*nm,		0);
	Glass1= Layer(    5, 1, dx2*nm,	   	0);
	dx1 = 200*rand(1)[1] + 100; dx2 = 200*rand(1)[1] + 100
	Si2 =   Layer( 11.9, 1, dx1*nm,	     	0);
	Glass2= Layer(    5, 1, dx2*nm,	   	0);
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

nω = 50*10^3; smoothing = 20

toppath = "./testing"
mkfolder(toppath)

for i in 1:5
	name="test$i"	
	path = toppath*"/example-"*name
	mkfolder(path)
	chip = genRandomStack()
	
	main(chip,path,name,nω,smoothing)
end

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



