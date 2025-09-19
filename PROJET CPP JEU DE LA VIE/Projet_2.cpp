////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////.
////////////////////////////////////////////// LE JEU DE LA VIE ////////////////////////////////////////////////////////.
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////.
////////////////////Inclusion des fichier, bibliothèques, namespace et instances de classes/////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////.

//Bibliothèques externes (SFML -> Rendu graphique, GTEST -> Tests unitaires)
#include <SFML/Graphics.hpp>
#include <gtest/gtest.h>
//Bibliothèque internes (entrées/sorties, gestiosn de fichiers, vecteurs...)
#include <iostream>
#include <vector>
#include <ctime>
#include <stdio.h>
#include <string>
#include <filesystem>
//Inclusions des classes
#include "Fichier.h"
#include "Ligne.h"
//Utilisation de cette notation pour les cout,endl, vecteurs ...
using namespace std;
//instance de la classe Fichier dans le main
Fichier fichier;

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////.
////////////////////////////Initialisation des valeurs (par défaut)/////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////.

const int cellSize = 50;  //taille des cellules
const int gridWidth = 10;  //nombre de cellules en largeur (valeur présentes dans la première ligen du fichier texte)
const int gridHeight = 10;  //nombre de cellules en hauteur (valeur présentes dans la première ligen du fichier texte)

vector<vector<int> > grid(gridWidth, vector<int>(gridHeight));

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////.
////////////////////////////Appel de l'ouverture du fichier/////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////.

string txt = fichier.lecture();
vector<string> liste = fichier.vecteur(txt);
Ligne jeu(liste);

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////.
////////////////////////////Affichage de la grille à l'écran////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////.

// Fonction pour convertir la grille fournie par le méthode fichier.vecteur
vector<vector<int>> convertirGrille(const vector<string>& grille) {
    vector<vector<int>> grid;
    for (const auto& ligne : grille) {
        vector<int> row;
        for (char c : ligne) {
            if (c == '0' || c == '1') {
                row.push_back(c - '0');
            }
        }
        grid.push_back(row);
    }
    return grid;
}

// Fonction pour afficher la grille avec SFML
void afficherAvecSFML(const vector<vector<int>>& grid, int cellSize) {
    if (grid.empty()) return; // Vérifier si la grille est vide
    sf::RenderWindow window(sf::VideoMode(grid[0].size() * cellSize, grid.size() * cellSize), "Game of Life");// Créer une fenêtre SFML
    sf::Clock clock;
    while (window.isOpen()) {// Dessiner la grille
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                window.close();
            }
            if (clock.getElapsedTime().asSeconds() > 2) {// Ferme la fenêtre après n secondes
                window.close();
            }
        }
        window.clear();
        sf::RectangleShape cell(sf::Vector2f(cellSize - 1, cellSize - 1));
        for (size_t y = 0; y < grid.size(); ++y) {
            for (size_t x = 0; x < grid[y].size(); ++x) {
                if (grid[y][x] == 1) {
                    cell.setPosition(x * cellSize, y * cellSize);
                    cell.setFillColor(sf::Color::White); // Cellules vivantes en vert
                    window.draw(cell);
                }
            }
        }
        window.display();
        sf::sleep(sf::milliseconds(500)); // Attente entre les affichages
    }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////.
//////////////////////////////////////////Test unitaires////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////.

// Test de la fonction `Fichier::lecture`
TEST(FichierTest, LectureFichier) {
    Fichier fichier;
    string contenu = fichier.lecture();
    EXPECT_FALSE(contenu.empty()) << "Le contenu du fichier ne doit pas être vide.";
}

// Test de la fonction `Fichier::vecteur`
TEST(FichierTest, ConversionVecteur) {
    Fichier fichier;
    string contenu = "5 5\n10101\n01010\n10101\n01010\n";
    vector<string> vecteur = fichier.vecteur(contenu);

    EXPECT_EQ(vecteur.size(), 5) << "Le vecteur doit contenir 5 lignes.";
    EXPECT_EQ(vecteur[1], "10101") << "La deuxième ligne doit être '10101'.";
}

// Test du constructeur de la classe `Ligne`(pas  le constucteur par défaut)
TEST(LigneTest, ConstructionLigne) {
    vector<string> grille = {"10101", "01010", "10101", "01010"};
    Ligne jeu(grille);

    EXPECT_EQ(jeu.grille.size(), 4) << "La grille doit contenir 4 lignes.";
    EXPECT_EQ(jeu.grille[0], "10101") << "La première ligne de la grille doit être '10101'.";
}

// Test de la fonction `Ligne::CompteCell`
TEST(LigneTest, CompteCell) {
    vector<string> grille = {"101", "010", "101"};
    Ligne jeu(grille);

    int voisins = jeu.CompteCell(1, 1, grille);
    EXPECT_EQ(voisins, 4) << "La cellule (1,1) doit avoir 4 voisins vivants.";
}

// Test de la fonction `Ligne::Generation`
TEST(LigneTest, Generation) {
    vector<string> grille = {"000", "111", "000"};
    Ligne jeu(grille);

    jeu.change_etat();
    EXPECT_EQ(jeu.grille[1], "010") << "Après une génération, la ligne du milieu doit être '010'.";
}

// Test de la conversion de grille pour SFML
TEST(ConversionGrilleTest, ConvertirGrille) {
    vector<string> grille = {"101", "010", "101"};
    vector<vector<int>> grid = convertirGrille(grille);

    EXPECT_EQ(grid.size(), 3) << "La grille convertie doit avoir 3 lignes.";
    EXPECT_EQ(grid[0][1], 0) << "La deuxième cellule de la première ligne doit être 0.";
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////.
/////////////////////////////////////Main (appel de méthodes)///////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////.

int main(int argc, char** argv) {
    ////////////////////////////////Lancement des tests unitaires///////////////////////////////////////////////////////
    cout<<"Initialisation des tests unitaires...\n"<<endl;
    ::testing::InitGoogleTest(&argc, argv);

    if (argc > 1 && string(argv[1]) == "--run-sfml") {
        cout<<"Lancement de la fenêtre SFML...\n"<<endl;
    }

    cout<<"Exécution des tests unitaires...\n"<<endl;
    int testResult = RUN_ALL_TESTS();

    cout<<"Tous les tests unitaires sont terminés.\n"<<endl;
    cout<<"Résultat des tests : " << (testResult == 0 ? "Tous validés !" : "Échec.") << "\n"<<endl;
    ////////////////////////////////Lancement du programme du jeu de la vie/////////////////////////////////////////////
    cout<<"Combien d'itérations voulez-vous réaliser ? \t" <<endl;
    int iteration = 5;
    cout<<iteration<<endl;

    cout<<"Comment voulez-vous obtenir le résultat ? \t 1. mode console \t 2. mode graphique"<<endl;
    int mode = 2;
    cout<<mode<<endl;

    while (iteration > 0) {
        if (mode == 1) {
            string fichierEntree = "grille.txt";
            string txt = fichier.lecture();
            string dossierSortie = fichierEntree + "_out";
            filesystem::create_directory(dossierSortie);
            //string txt = fichier.lecture();
            vector<string> liste = fichier.vecteur(txt);
            for (const auto& ligne : liste) {
                cout<<ligne<<endl;
            }
            liste.erase(liste.begin());
            Ligne jeu(liste);
            for (int i = 0; i < 5; ++i) {
                cout<<"Iteration : "<< i + 1 << "\n"<<endl;
                jeu.change_etat();
                jeu.AfficheGrille();
                string fichierIteration = dossierSortie + "/iteration_" + to_string(i + 1) + ".txt";
                fichier.ecriture(fichierIteration, jeu.grille);
            }
        }

        if (mode == 2) {
            Fichier fichier;
            string txt = fichier.lecture();
            vector<string> liste = fichier.vecteur(txt);

            for (const auto& ligne : liste) {
                cout<<ligne<<endl;
            }

            liste.erase(liste.begin());

            Ligne jeu(liste);

            for (int i = 0; i < 5; ++i) {
                jeu.change_etat();
                vector<vector<int>> grid = convertirGrille(jeu.grille);
                afficherAvecSFML(grid, cellSize); // Afficher la grille avec SFML
            }
            return 0;
        }
    }
    return testResult;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////.
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////.
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////.