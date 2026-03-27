# Guide de développement multi-versions — is_test_versions

Ce document explique comment travailler sur ce module Odoo en parallèle sur plusieurs versions (16.0, 18.0, 19.0).

## Structure du dépôt

Le module `is_test_versions` utilise **une branche git par version d'Odoo** (convention Odoo / OCA) :

| Branche | Version Odoo | `__manifest__.py` version |
|---------|-------------|--------------------------|
| `16.0`  | Odoo 16     | `16.0.0.0.1`             |
| `18.0`  | Odoo 18     | `18.0.0.0.1`             |
| `19.0`  | Odoo 19     | `19.0.0.0.1`             |

La branche par défaut sur GitHub est `19.0` (dernière version).

## Prérequis

- Les sources Odoo de chaque version sont installées localement :
  ```
  dev_odoo/
  ├── 16.0/0-odoo16/    # Sources Odoo 16
  ├── 18.0/0-odoo18/    # Sources Odoo 18
  └── 19.0/0-odoo19/    # Sources Odoo 19
  ```
- Un environnement Python (venv) par version d'Odoo.
- PostgreSQL installé avec un utilisateur/base par version.

## 1. Mise en place des worktrees

Plutôt que de faire des `git checkout` entre les branches, on utilise **git worktree** pour avoir les 3 branches en même temps sur le disque :

```bash
# Cloner le dépôt sur la branche 19.0 (branche par défaut)
cd ~/Documents/Développement/dev_odoo
git clone git@github.com:tonygalmiche/is_test_versions.git 19.0/is_test_versions

# Créer les worktrees pour les autres versions
cd 19.0/is_test_versions
git worktree add ../../16.0/is_test_versions 16.0
git worktree add ../../18.0/is_test_versions 18.0
```

Résultat :

```
dev_odoo/
├── 16.0/
│   ├── 0-odoo16/
│   └── is_test_versions/   ← branche 16.0 (worktree)
├── 18.0/
│   ├── 0-odoo18/
│   └── is_test_versions/   ← branche 18.0 (worktree)
└── 19.0/
    ├── 0-odoo19/
    └── is_test_versions/   ← branche 19.0 (repo principal)
```

> **Avantage** : pas besoin de changer de branche, les 3 versions coexistent. On édite directement dans le bon dossier.

## 2. Environnements Python

Chaque version d'Odoo nécessite son propre environnement Python :

```bash
# Odoo 16 (Python 3.10)
cd ~/Documents/Développement/dev_odoo/16.0/0-odoo16
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

# Odoo 18 (Python 3.12)
cd ~/Documents/Développement/dev_odoo/18.0/0-odoo18
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

# Odoo 19 (Python 3.12)
cd ~/Documents/Développement/dev_odoo/19.0/0-odoo19
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

## 3. Fichiers de configuration

Créer un fichier `.conf` par version avec un **port HTTP différent** et une **base de données distincte**.

### `16.0/odoo16.conf`

```ini
[options]
db_host = localhost
db_port = 5432
db_user = odoo16
db_password = odoo16
db_name = odoo16_test
http_port = 8016
addons_path = /home/tony/Documents/Développement/dev_odoo/16.0/0-odoo16/addons,/home/tony/Documents/Développement/dev_odoo/16.0/is_test_versions
```

### `18.0/odoo18.conf`

```ini
[options]
db_host = localhost
db_port = 5432
db_user = odoo18
db_password = odoo18
db_name = odoo18_test
http_port = 8018
addons_path = /home/tony/Documents/Développement/dev_odoo/18.0/0-odoo18/addons,/home/tony/Documents/Développement/dev_odoo/18.0/is_test_versions
```

### `19.0/odoo19.conf`

```ini
[options]
db_host = localhost
db_port = 5432
db_user = odoo19
db_password = odoo19
db_name = odoo19_test
http_port = 8019
addons_path = /home/tony/Documents/Développement/dev_odoo/19.0/0-odoo19/addons,/home/tony/Documents/Développement/dev_odoo/19.0/is_test_versions
```

> **Note** : adapter `addons_path` si vous avez d'autres modules personnalisés à inclure.

## 4. Scripts de lancement

Créer un script shell par version pour simplifier le lancement :

### `run16.sh`

```bash
#!/bin/bash
cd ~/Documents/Développement/dev_odoo/16.0/0-odoo16
source venv/bin/activate
./odoo-bin -c ../odoo16.conf "$@"
```

### `run18.sh`

```bash
#!/bin/bash
cd ~/Documents/Développement/dev_odoo/18.0/0-odoo18
source venv/bin/activate
./odoo-bin -c ../odoo18.conf "$@"
```

### `run19.sh`

```bash
#!/bin/bash
cd ~/Documents/Développement/dev_odoo/19.0/0-odoo19
source venv/bin/activate
./odoo-bin -c ../odoo19.conf "$@"
```

Rendre les scripts exécutables :

```bash
chmod +x run16.sh run18.sh run19.sh
```

## 5. Utilisation quotidienne

### Lancer Odoo

```bash
# Lancer une version
./run18.sh

# Lancer avec mise à jour du module
./run18.sh -u is_test_versions

# Les 3 en parallèle (dans 3 terminaux différents)
./run16.sh
./run18.sh
./run19.sh
```

### Accéder aux instances

| Version | URL                      |
|---------|--------------------------|
| Odoo 16 | http://localhost:8016    |
| Odoo 18 | http://localhost:8018    |
| Odoo 19 | http://localhost:8019    |

### Développer

1. **Éditer** le code directement dans le worktree de la version ciblée (ex : `18.0/is_test_versions/`).
2. **Tester** en relançant Odoo avec `-u is_test_versions`.
3. **Commiter** depuis n'importe quel worktree (c'est le même dépôt git).
4. **Pousser** :
   ```bash
   git push origin 16.0 18.0 19.0
   ```

### Reporter un fix sur plusieurs versions

```bash
# Depuis le worktree de la version cible
cd ~/Documents/Développement/dev_odoo/16.0/is_test_versions
git cherry-pick <sha_du_commit>
```

### Gérer les worktrees

```bash
# Lister les worktrees
git worktree list

# Supprimer un worktree
git worktree remove ../../16.0/is_test_versions
```

## 6. Conventions

- Chaque branche versionnée (`16.0`, `18.0`, `19.0`) contient le code adapté à la version d'Odoo correspondante.
- Le fichier `__manifest__.py` doit toujours refléter la bonne version (`'version': 'XX.0.0.0.1'`).
- Le fichier `README.md` de chaque branche indique la version d'Odoo ciblée.
- Quand une nouvelle version d'Odoo sort, créer une nouvelle branche à partir de la dernière version.
