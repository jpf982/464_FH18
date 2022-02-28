

#install julia & graphics

echo "Installing Julia programming language, QT for graphics"
#sudo apt-get install julia
#sudo apt-get install qt5-default
#sudo apt-get install python3-tk

echo "Installing python3 plotting software"
pip install matplotlib

echo "Installing necessary julia packages..."
julia << EOF
using Pkg

Pkg.add("LinearAlgebra")
Pkg.add("Arpack")
Pkg.add("Plots")
Pkg.add("PyPlot")
Pkg.add("Interpolations")
Pkg.add("Distributions")
Pkg.add("ColorSchemes")
EOF


echo "Installing julia-vim with LaTeX support"
cd ~/.vim
mkdir -p pack/plugins/start && cd pack/plugins/start
git clone git://github.com/JuliaEditorSupport/julia-vim.git

