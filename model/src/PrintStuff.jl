
module PrintStuff
using Printf
using UsefulFunctions

export PrintStack, PrintTransmission

function PrintStack(stack, path, name)
	fname = "stack.txt"
	Nlayers = size(stack)[1]
	Δz = thickness(stack)*10^(-3)
	open(path*"/"*fname, "w") do f
		println(f,"Name_stack = $name")
		println(f,"#_layers = $Nlayers")
		println(f,"total thickness (nm)  = $Δz")
		println(f,"# Layer key: name, rel. permittivity, rel. permeability, height (nm), dep time (min)")
		for layer in stack
			#@printf ("L-%i_S-%g_dh0-%g_fu-%g_theta-%g_U-%g_mu-%g_V0-%g_U2-%g",λ,σ,Δh0,fᵤ,θ,U,μ,V₀,U₂)
			name = layer.name; er = layer.εᵣ; ur = layer.μᵣ; dx = layer.Δx*10^9;
			if(name == "Si")
				v = 4.5 # m/s
			elseif(name == "Glass")
				v = 43
			else
				v = 10^9
			end
			time = dx/(v)
			println(f, "$name \t $er \t $ur \t $dx \t $time")
		end
	end
	println("Stack details printed to .$path/$fname")
end

function PrintTransmission(Tvals,ωvals,path, name="")
	fname = name*"transmission.txt"
	open(path*"/"*fname, "w") do f # open the file path/fname
		println(f, "Transmission\t ω (THz)")
		for i in eachindex(Tvals)
			println(f, "$(Tvals[i])\t$(ωvals[i])")
		end
	end
	close(path*fname)
	println("Transmission printed to .$path/$fname")
end

end
