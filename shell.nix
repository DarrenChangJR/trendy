with import <nixpkgs> {};

mkShell {
  nativeBuildInputs = [
    python3
    python3Packages.pip
    python3Packages.pandas
    python3Packages.plotly
    python3Packages.requests
  ];

  shellHook = ''
    echo "You are now using a NIX environment"
  '';
}
