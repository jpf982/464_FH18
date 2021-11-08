
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
		println(f,"total thickness (μm)  = $Δz")
		for layer in stack
			println(f, "$(layer)")
			println(f, "$layer")
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
