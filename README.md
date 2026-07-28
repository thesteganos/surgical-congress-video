# surgical-congress-video

A [Claude](https://claude.com) **Skill** that turns raw operating-room footage into a submission-ready **"vídeo livre"** for a medical congress — blinded, captioned, within the time limit — together with the companion scientific abstract (PT/EN), shot list and submission checklist.

Uma **Skill** do [Claude](https://claude.com) que transforma filmagem cirúrgica bruta em um **vídeo livre** pronto para submissão em congresso médico — anonimizado, legendado e dentro do limite de tempo — junto com o resumo científico (PT/EN), roteiro e checklist de submissão.

---

## 🇧🇷 Português

### O que faz

Produzir um vídeo livre para congresso a partir de 30–60 minutos de gravação de cirurgia envolve muito mais do que cortar clipes: é preciso ler o edital, respeitar o limite de tempo, garantir o anonimato exigido em avaliações às cegas, embasar o resumo na literatura e exportar nos formatos aceitos. Esta skill organiza esse processo do início ao fim.

**Entregáveis típicos:**

- Vídeo editado dentro do limite de tempo, com slides de título/créditos e **legendas** descrevendo cada etapa cirúrgica
- Duas resoluções de exportação (**720p** para upload, **1080p** para qualidade)
- **Resumo estruturado** em português e inglês
- **Roteiro** cronometrado e textos dos slides
- **Checklist de submissão**

### Fluxo de trabalho

1. **Ler o edital primeiro** — limite de tempo, submissão às cegas, formato, tamanho máximo, prazo. É o que define todo o resto.
2. **Pesquisar a literatura** — incidência, mecanismo, manejo e taxas de recidiva, para embasar o resumo e o slide de contexto.
3. **Reunir os dados do caso** — demografia, procedimento prévio, quadro, imagem, achados operatórios e desfecho.
4. **Anonimizar** — sem autor, instituição ou dados do paciente em nenhum slide; conferir os cantos da filmagem bruta.
5. **Escrever** resumo (PT/EN), roteiro, narração e textos dos slides.
6. **Selecionar os momentos-chave** com mosaicos de miniaturas — o cirurgião indica os intervalos por clipe.
7. **Gerar os slides** (1920×1080).
8. **Codificar e montar** os segmentos com legendas, acelerando levemente trechos longos para caber no limite.
9. **Exportar e conferir** 720p/1080p com uma folha de verificação de quadros.
10. **Entregar** com o passo a passo de submissão.

### Aviso

A skill automatiza o trabalho técnico e editorial. **O conteúdo médico, a indicação cirúrgica, a conferência dos dados do paciente e o cumprimento do edital são responsabilidade do cirurgião autor.** Sempre revise o vídeo final e o resumo antes de submeter, e siga as normas éticas e de privacidade aplicáveis (consentimento do paciente, anonimização, regulamento do congresso).

---

## 🇬🇧 English

### What it does

Producing a congress "free video" from 30–60 minutes of surgical recording is more than trimming clips: you must read the regulation, respect the time limit, guarantee the anonymity required for blind review, ground the abstract in the literature, and export in the accepted formats. This skill organizes that process end to end.

**Typical deliverables:**

- Edited video within the time limit, with title/credits slides and **on-screen captions** for each surgical step
- Two export resolutions (**720p** for upload, **1080p** for quality)
- **Structured abstract** in Portuguese and English
- Timestamped **shot list** and slide texts
- **Submission checklist**

### Workflow

1. **Read the regulation first** — time limit, blind submission, format, max file size, deadline. It dictates everything else.
2. **Search the literature** — incidence, mechanism, management and recurrence rates, to ground the abstract and context slide.
3. **Gather case data** — demographics, index procedure, presentation, imaging, operative findings and outcome.
4. **Anonymize** — no author, institution or patient data on any slide; check the raw footage corners.
5. **Write** the abstract (PT/EN), shot list, narration and slide texts.
6. **Pick key moments** via thumbnail contact sheets — the surgeon returns keep-ranges per clip.
7. **Build the slides** (1920×1080).
8. **Encode and assemble** segments with captions, mildly speeding up long stretches to fit the limit.
9. **Export and verify** 720p/1080p with a frame contact sheet.
10. **Hand off** with a submission step-by-step.

### Disclaimer

This skill automates the technical and editorial work. **Medical content, surgical indication, verification of patient data, and compliance with the congress regulation remain the responsibility of the submitting surgeon.** Always review the final video and abstract before submitting, and follow applicable ethics and privacy rules (patient consent, anonymization, congress regulation).

---

## Installation / Instalação

**Claude Code / Cowork** — copy this folder into your skills directory:

```bash
git clone https://github.com/thesteganos/surgical-congress-video.git
cp -r surgical-congress-video ~/.claude/skills/
```

Then just ask, e.g. *"monta o vídeo livre do meu caso pro congresso"* / *"cut this surgery video down to 7 minutes for a congress"*.

## Repository contents / Conteúdo

```
SKILL.md                                  # the skill itself / a skill
scripts/make_contact_sheets.sh            # thumbnail mosaics / mosaicos de miniaturas
scripts/make_slides.py                    # 1920x1080 slide PNGs / slides em PNG
scripts/build_video.py                    # encode segments + concat / codifica e monta
references/ffmpeg_and_sandbox_notes.md    # ffmpeg recipes & gotchas / receitas e armadilhas
```

## Requirements / Requisitos

`ffmpeg` + `ffprobe`, Python 3 with **Pillow**, and DejaVu fonts (or adjust the font path in the scripts).

## License / Licença

MIT — see [LICENSE](LICENSE).
