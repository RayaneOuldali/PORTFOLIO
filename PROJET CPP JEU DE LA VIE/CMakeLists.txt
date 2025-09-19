cmake_minimum_required(VERSION 3.15)
project(Projet_2 LANGUAGES CXX)

# Définir les options de compilation
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "-g -Wall -Werror")

# Spécifier les chemins vers SFML
set(SFML_INCLUDE_DIR "C:/Users/thais/Bibli_SFML_c++/SFML-2.6.2-windows-gcc-13.1.0-mingw-64-bit/SFML-2.6.2/include")
set(SFML_LIBRARY_DIR "C:/Users/thais/Bibli_SFML_c++/SFML-2.6.2-windows-gcc-13.1.0-mingw-64-bit/SFML-2.6.2/lib")

# Inclure les fichiers d'en-tête et de bibliothèque SFML
include_directories(${SFML_INCLUDE_DIR})
link_directories(${SFML_LIBRARY_DIR})

# Ajouter les fichiers source
file(GLOB_RECURSE SRCS "Projet_2.cpp")

# Ajouter l'exécutable principal
add_executable(SFMLTest ${SRCS} Projet_2.cpp)

# Chemin vers le répertoire Google Test
set(GTEST_DIR "C:/Users/thais/Documents Local/CPI A2/Projet 2/Livrable/Projet-2/cmake-build-debug/googletest/googletest-main")

# Ajouter Google Test comme sous-dossier
add_subdirectory(${GTEST_DIR} googletest)

# Inclure les répertoires de Google Test
include_directories(${GTEST_DIR}/googletest/include)
include_directories(${GTEST_DIR}/googlemock/include)

# Ajouter un exécutable pour les tests unitaires
add_executable(UnitTests Projet_2.cpp
        Fichier.cpp
        Ligne.cpp
        Grille.cpp)

# Lier les bibliothèques SFML
target_link_libraries(SFMLTest sfml-graphics sfml-window sfml-audio sfml-network sfml-system)

# Lier Google Test ET SFML aux tests unitaires
target_link_libraries(UnitTests gtest gtest_main sfml-graphics sfml-window sfml-audio sfml-network sfml-system)