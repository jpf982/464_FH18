push!(LOAD_PATH, "./")

module Dielectric

using LinearAlgebra
using Arpack
using Constants
using Interpolations
using PyPlot

export ε_mat

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
E₁ = 0*eV; E₂ = 9*eV
Egrid = E₁:dE:E₂
A = 43.1409 # taken from my DFT homework
g(x,μ,σ) = exp(-(x-μ)^2/(2*σ^2))
l(x,μ,w) = w^2/(4*(x-μ)^2 + w^2)
#ε₂si(E) = 35*g(E,3.2,0.3) + 40*g(E,4.5,0.5) + 10*g(E,5.2,0.4)
ε₂si(E) = 25*l(E,3.2,0.2) + 25*g(E,3.65,0.25) + 35*l(E,4.1,0.3) + 10*l(E,5.2,2)
#ε₂si(E) = *exp(-(E-4)^2/2)
ε₂ = ε₂si.(Egrid)


println("Pre-calculating Kramers-Kronig ε₁(ω). Performing integral, please hold.")
#ε₁si(E) = 1 + (2/π)*∫( (ε₂), Egrid, 0,dE,E)
ε₁si(E) = 1 + (2/π)*∫( (ε₂.*Egrid ./ (Egrid.^2 .- E^2)), Egrid, E₁, dE, E-ΔE) + 
              (2/π)*∫( (ε₂.*Egrid ./ (Egrid.^2 .- E^2)), Egrid, E+ΔE, dE, E₂)
ε₁ = ε₁si.(Egrid)
println("Done!")

ε₁intp = LinearInterpolation(Egrid,ε₁)
ε₂intp = LinearInterpolation(Egrid,ε₂)

#=println("Plotting..")
plot(Egrid,ε₁)
plot(Egrid,ε₂)
fig = gcf()
display(fig)
#plot!(Egrid,ε₁)=#


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
