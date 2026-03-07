Reflection:

The Makefile makes the dependency relationships between different parts
of the project explicit, which run_all.sh left implicit. In run_all.sh,
every step runs every time, even if nothing relevant changed, and it is
not obvious which files depend on which. 

The Makefile clearly shows how the figures, tables, and final paper are
connected, and Make automatically rebuilds only what is necessary when a
file is modified. This makes the workflow more efficient and easier for a
new collaborator to understand. 

OVerall, the Makefile documents the structure of the project in a way that
the script does not. 
