with import <nixpkgs> {};

mkShell {
  nativeBuildInputs = [
    python3
    python3Packages.pip
    python3Packages.pandas
    python3Packages.plotly
    python3Packages.requests
    python3Packages.matplotlib
  ];

  shellHook = ''
    echo "You are now using a NIX environment"
  '';
}
