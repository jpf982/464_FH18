push!(LOAD_PATH, "./")
push!(LOAD_PATH, "./src/")

using thinfilm
using Printf

function mkfolder(path)
	if(isdir(path))
		println("$path already exists...")
		#rm(path, recursive=true)
	else
		mkdir(path)
	end
end




#λ = 21; σ = 1.5*nm; Δh0 = 0.7*nm; θ = 0; fᵤ = 0.0; U = 0*eV; μ = 0*eV; V₀ = 0.00*eV; U₂ = 0.00*eV
#main(λ, σ, Δh0, fᵤ, U, μ, U₂)

toppath = "./testing"
mkfolder(toppath)

name = "testing"
path = toppath*"/10-28-2020-"*name
mkfolder(path)

main(path,name)
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



