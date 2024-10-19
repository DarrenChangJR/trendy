# mkdir <project_name>
# cp template_shell.nix <project_name>/shell.nix
# cd <project_name>
# nix-shell

with import <nixpkgs> {};

mkShell {
  venvDir = "./.venv";
  buildInputs = [
    python3
    python3.pkgs.venvShellHook
  ];
  NIX_LD_LIBRARY_PATH = lib.makeLibraryPath [
    # Add pkgs whose side-effects add any required .so files
    stdenv.cc.cc
    zlib
  ];
  NIX_LD = lib.fileContents "${stdenv.cc}/nix-support/dynamic-linker";
  shellHook = ''
    export LD_LIBRARY_PATH=$NIX_LD_LIBRARY_PATH
    venvShellHook
  '';
}
