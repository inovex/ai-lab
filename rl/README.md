# AI Lab HSKA: Reinforcement Learning

Praktische Herangehensweise an die Lösung unterschiedlich komplexer Kontroll-Probleme mit Hilfe von modernen Reinforcement Learning (RL) Algorithmen. Von tabellarischen Methoden wie Q-Learning bis hin zur Funktionsapproximation durch Neuronale Netze soll versucht werden, Agenten in verschiedenen OpenAI Gym Umgebungen zu trainieren. Das Hauptziel am Ende ist es ein Atari Game mit Deep RL zu bewältigen.

## Vorbereitung

Jupyter Notebook inkl. TensorBoard starten:

```bash
docker-compose up ai-lab-rl-gpu  # Uses NVIDIA GPU
docker-compose up ai-lab-rl-cpu  # For CPU usage
```

### Ohne docker-compose

Docker Image bauen:

```bash
docker build -f gpu.Dockerfile -t ai-lab-rl .
```

Docker starten:

```bash
docker run -it --rm -v $PWD:/rl -p 8888:8888 --gpus all ai-lab-rl
```

### Jupyter Lab

Im Browser `http://localhost:8888` aufrufen.
**Speichern klappt nur bei Tusted Notebooks!**

### TensorBoard

Im Browser `http://localhost:6006` aufrufen.

## Termine

| Datum | Inhalt |
|-|-|
| 29.05.2020 | Vorstellung Aufgabenteil 1: CliffWalking und CartPole mit Q-Learning |
| 05.06.2020 | Ferien (Pfingstwoche) |
| 12.06.2020 | Remotebetreuung |
| 19.06.2020 | Abgabe Aufgabenteil 1 und Vorstellung Aufgabenteil 2: CartPole und Atari Gym mit DQN (pixel-basierter State-Space) |
| 26.06.2020 | Remotebetreuung |
| 03.07.2020 | Abgabe Aufgabenteil 2 |

## Hinweise

### Alle Ausgabezellen löschen

```bash
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace Notebook.ipynb
```

### Package als root temporär in vorhandenem Container installieren

```bash
docker exec -u 0 -it <container_id> /bin/bash
```

## Weiterführende Lektüre

- "Standard"-Lektüre für den Einstieg in RL: [Reinforcement Learning: An Introduction (Richard S. Sutton and Andrew G. Barto)](http://incompleteideas.net/book/RLbook2018.pdf)
- Ausführlich und gut erklärter Einstieg in RL (Video-Lektionen) von David Silver (Google DeepMind): [UCL Course on RL (David Silver)](http://www0.cs.ucl.ac.uk/staff/D.Silver/web/Teaching.html)
- [Algorithms in Reinforcement Learning (Csaba Szepesvári)](https://sites.ualberta.ca/~szepesva/papers/RLAlgsInMDPs.pdf)
- Blog mit Videos zum Einstieg in RL und Q-Learning, DQN und vieles mehr: [Reinforcement Learning - Introducing Goal Oriented Intelligence](https://deeplizard.com/learn/video/nyjbcRQ-uQ8)