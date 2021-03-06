push!(LOAD_PATH, "./")

module Dielectric

using LinearAlgebra
using Arpack
using Constants
using Interpolations
using UsefulFunctions
using PyPlot

export ε_mat,plotkk

function ∫(fgrid,xgrid,x₁,dx,x₂)
	sum = 0
	for i in eachindex(xgrid)
		x = xgrid[i]
		if(x > x₁ && x < x₂)
			y = fgrid[i]
			sum += y*dx
		end
	end
	return sum
end
		

dE = 0.0005*eV
ΔE = 10*dE
E₁ = 0*eV; E₂ = 20*eV
Egrid = E₁:dE:E₂
A = 43.1409 # taken from my DFT homework
g(x,μ,σ) = exp(-(x-μ)^2/(2*σ^2)) - exp(-(-μ)^2/(2*σ^2))
g₀(x,μ,σ) = exp(-(x-μ)^2/(2*σ^2))
l(x,μ,w) = w^2/(4*(x-μ)^2 + w^2) - w^2/(4*(0-μ)^2 + w^2)

# perfect Si
#ε₂si(E) = 25*l(E,3.2,0.2) + 25*g(E,3.65,0.25) + 35*l(E,4.1,0.3) + 10*l(E,5.2,2)

# c-Si
#ε₂si(E) = 20*l(E,3.4,0.5) + 48*l(E,4.2,1.2)

# nc-Si
#ε₂si(E) = 3*g(E,3.4,0.2) + 35*g(E,4.35,1.0)

# α-Si
ε₂si(E) = 20*g₀(E,3.4,2.5) - 5*g₀(E,0,0.5)
ε₂si(E) = 20*g₀(E,3.4,2.5) - 5*g₀(E,0,0.5)

ε₂ = ε₂si.(Egrid)


println("Pre-calculating Kramers-Kronig ε₁(ω). Performing integral, please hold.")
#ε₁si(E) = 1 + (2/π)*∫( (ε₂), Egrid, 0,dE,E)
ε₁si(E) = 1 + (2/π)*∫( (ε₂.*Egrid ./ (Egrid.^2 .- E^2)), Egrid, E₁, dE, E-ΔE) + 
              (2/π)*∫( (ε₂.*Egrid ./ (Egrid.^2 .- E^2)), Egrid, E+ΔE, dE, E₂)
ε₁ = movingaverage(ε₁si.(Egrid),15)
println("Done!")

ε₁intp = LinearInterpolation(Egrid,ε₁)
ε₂intp = LinearInterpolation(Egrid,ε₂)

#=println("Plotting..")
#plot!(Egrid,ε₁)=#
function plotkk()
	plot(Egrid,ε₁)
	plot(Egrid,ε₂)
	fig = gcf()
	display(fig)
end

plotkk()


function ε_mat(material)
	if(material == "SiO2" || material == "Glass" || material == "Substrate")
		# okay this is extremely jank, idk how else to get the compiler to return ε(ω). Rewrite this.
		return (ε = ω -> 5)
	elseif(material == "Air")
		return (ε = ω -> 1)
	elseif(material == "Si")
		return (ε = ω -> ε₁intp(ω*ħ) + im*ε₂intp(ω*ħ))
	end
end

end
