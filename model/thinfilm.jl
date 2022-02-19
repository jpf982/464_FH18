push!(LOAD_PATH, "./src/")

module thinfilm
using LinearAlgebra
using Constants
using ConstructHamiltonian
using UsefulFunctions
using PlotStuff
using PrintStuff
using Transmit
using Dielectric


#=
# So, 
# 
=#
export main, Layer, thickness

struct Layer 
	name # name of system
	εᵣ #electric permeability
	μᵣ  #magnetic permeability
	Δx #thickness in nm
	σ # electrical conductivity
end

function thickness(stack)
	return 10^9*sum([L.Δx for L in stack])
end



function getTransmissionVsAngle(layers, ω_begin, ω_end, nω, θ_begin, θ_end, nθ, path, name, avg=0)
	println("\nSolving Eqs to generate T(ω,θ) for $name...")
	pwSolver = pwCoeffs(layers,false);
	Nlayers = size(layers)[1];
	ω₁ = ω_begin/THz; ω₂ = ω_end/THz;
	println("Probing transmission for $nω points for ω = [$ω₁, $ω₂] THz")
	println("for $nθ points for θ ∈ [$θ_begin, $θ_end] degrees")
	degToRad = π/180
	θVals = collect(LinRange(θ_begin*degToRad,θ_end*degToRad,nθ))
	spectra = zeros(nθ,nω)
	if(avg > 0)
		avgspectra = zeros(nθ,nω)
	end
	for i in eachindex(θVals)
		Tvals, ωvals = transmission(pwSolver,Nlayers,ω_begin,ω_end,nω,θVals[i]);
		spectra[i,:] = Tvals
		if(avg > 0) 
			avgTvals = movingaverage(Tvals, avg) 
			avgspectra[i,:] = avgTvals
		end
	end
	PrintStack(layers,path,name)
	fig = plot2D(spectra',θ_begin,θ_end,ω_begin*ħ/q,ω_end*ħ/q,"Angle (°)","E (eV)","inferno","T(θ,E)")
	SaveFigure(fig,path,"spectrum_angle")
	if(avg > 0)
		fig = plot2D(avgspectra',θ_begin,θ_end,ω_begin*ħ/q,ω_end*ħ/q,"Angle (°)","E (eV)","inferno","T(θ,E)")
		SaveFigure(fig,path,"avgspectrum_angle")
	end
	return spectra
end


function getTransmission(layers, ω_begin, ω_end, nω, path, name, avg=0)
	println("\nSolving Eqs to generate T(ω) for $name...")
	pwSolver = pwCoeffs(layers,false);
	Nlayers = size(layers)[1];
	ω₁ = ω_begin/THz; ω₂ = ω_end/THz;
	println("Probing transmission for $nω points for ω = [$ω₁, $ω₂] THz")
	Tvals, ωvals = transmission(pwSolver,Nlayers,ω_begin,ω_end,nω);
	if(avg > 0) 
		avgTvals = movingaverage(Tvals, avg) 
		PrintTransmission(Tvals,ωvals,path,"smooth")
		fig = plot1D(ωvals,avgTvals,0,1,"ω (THz)","Transmission (smooth)")
		SaveFigure(fig,path,"smooth_spectrum")
	end
	PrintStack(layers,path,name)
	PrintTransmission(Tvals,ωvals,path)
	fig = plot1D(ωvals,Tvals,0,1,"ω (THz)","Transmission")
	SaveFigure(fig,path,"spectrum")
	return Tvals
end


#param of layer: εᵣ  μᵣ  Δx (nm), σ (S/m)


#=Air  = Layer(     1, 1, 800*nm,		0);
GaAs = Layer( 12.25, 1, 200*nm,		0);
Si1 =   Layer( 11.9, 1, 200*nm,		0);
Substrate=Layer(  5, 1,10^6*nm,    	0);
Glass1=Layer(     5, 1, 200*nm,	   	0);
Si2 =   Layer( 11.9, 1, 500*nm,	     	0);
Glass2=Layer(     5, 1, 300*nm,	   	0);

PhC₁ = [
	Glass1,
	Si1,
	Glass1,
	Si1,
	Glass1,
	Si1,
	Glass1,
	Si1,
	Glass1,
	Si1,
	Glass1,
	Si1,
	Glass1,
	Si1,
	Glass1,
	Si1,
	]
PhC₂ = [
	Si2,
	Glass2,
	Si2,
	Glass2,
	Si2,
	Glass2,
	Si2,
	Glass2,
	Si2,
	]

TPhQ = vcat(Air,PhC₁,PhC₂,Air)
chip = vcat(Air,PhC₁,PhC₂,Substrate,Air)
=#

function main(stack,path,name,nω,smoothing,θ_begin=0, θ_end=0, nθ=1)
	ω_begin = 0*THz
	ω_end = 6500*THz
	if(θ_end > 0 && nθ > 1)
		return getTransmissionVsAngle(stack, ω_begin, ω_end, nω, θ_begin, θ_end, nθ, path, name, smoothing)
	else
		return getTransmission(stack, ω_begin, ω_end, nω, path, name, smoothing)
	end
end

#main()

end
#=
klist = ["Γ", "M", "K", "Γ"]
nk = 1028
println("Getting eigenvalues of graphene between k = ")
show(klist)
println("...")
E, Estates = getBands(klist, nk, a, H)
#display(27.2*E)
println("Plotting...")
plotBands(klist,nk,E)
println("Done! Press ctrl+d to quit")
=#
