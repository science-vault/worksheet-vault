const placeholder = /^(?:extra worksheets|uncategorised|general|science|chemistry|physics|biology|level [123] (?:biology|chemistry|physics)\s*-?|practice exam)$/i;
const senior = [
  ['Biology', '12', 'Inheritance and Evolution', /punnett|pedigree|speciation|genetic variation|natural selection|allele frequenc|mendel|genetic drift|meiosis|genetic change|inheritance|mutation|biological evolution/],
  ['Biology', '12', 'Homeostasis and Disease', /homeostasis|thermoregulat|osmoregulat|immune response|infectious disease|feedback loops?|antibiotic resistance|pathogens/],
  ['Biology', '11', 'Ecosystems and Biodiversity', /ecology|food chains?|food webs?|succession|zonation|species interactions?|ecological pyramids?/],
  ['Biology', '11', 'Cells and Multicellular Organisms', /active transport|cell transport|facilitated diffusion|plasma membranes?|cell organelles|cell(?:ular)? respiration|aerobic respiration|gas exchange|cell structures?|osmosis/],
  ['Chemistry', '12', 'Equilibrium and Acids and Bases', /ionic product|\bpoh\b|buffer|titration curves?|equilibrium constant|le chatelier|weak acids?|weak bases?|aqueous equilibrium|acidic salts|acid.base equilibrium|conjugate (?:acid|base)/],
  ['Chemistry', '12', 'Redox and Electrochemistry', /electrolysis|electrolytic|galvanic|electrochem|cell diagrams|redox|oxidation number/],
  ['Chemistry', '12', 'Organic Chemistry and Chemical Synthesis', /esters?|amino acids|acid chlorides|carboxylic|spectra|spectroscopy|aldehydes|ketones|organic synthesis|saponification|amines|polymers|alcohol production/],
  ['Chemistry', '11', 'Reaction Rates', /collision theory|activation energy|rates? of reaction|reaction rates|catalysts?/],
  ['Chemistry', '11', 'Atomic Structure, Bonding and Materials', /periodic table|electron arrangement|atomic structure|ionic bond|ionic substances|covalent|molecular substances|intermolecular|atomic radius|periodic patterns|electron configuration|atomic models/],
  ['Chemistry', '11', 'Chemical Quantities and Solutions', /mole calculations|stoichiometr|empirical formula|dilution|solubility|precipitation|standard solution|molar mass/],
  ['Physics', '12', 'Gravity, Projectiles and Circular Motion', /centripetal|projectile|satellites?|orbital motion|gravitation/],
  ['Physics', '12', 'Electromagnetism', /solenoids?|magnetic fields?|electromagnet|generators?|transformers?|electric field lines|electrostatic forces/],
  ['Physics', '11', 'Waves', /waves?|refraction|reflection|dispersion|apparent depth|sound|ripple tank|mirrors?|lenses|period calculations/],
  ['Physics', '11', 'Nuclear Physics', /nuclear|radiation penetration|radioactiv|half.life|fusion reactions|fission|ionisation|rutherford|alpha and beta/],
  ['Physics', '11', 'Electrical Circuits', /circuits?|ohmic|conductors?|current electricity|resistance|voltage/],
  ['Physics', '11', 'Heating and Energy Transfers', /specific heat|heating|latent heat|heat transfer|convection/],
  ['Physics', '11', 'Motion and Forces', /acceleration|mechanics|momentum|motion|forces?|energy transformations|power calculations|equilibrium and|pressure|adding vectors|speed.velocity|work and power/],
];
const juniorScience = [
  ['7', 'Chemical Sciences', 'Particle Model and Separating Mixtures', /particle model|separat\w* mixtures?|filtration and|chromatograph|states of matter/],
  ['7', 'Biological Sciences', 'Classification and Identification Keys', /dichotomous|classification of|classifying (?:living|animals|organisms)/],
  ['7', 'Biological Sciences', 'Food Chains, Food Webs and Energy Flow', /food chains?|food webs?/],
  ['7', 'Physical Sciences', 'Forces and Simple Machines', /simple machines?|\blevers?\b|pulleys?/],
  ['7', 'Earth and Space Sciences', 'Earth, Sun, Moon and the Solar System', /phases of the moon|solar system|the moon|eclipses?|\btides\b/],
  ['8', 'Biological Sciences', 'Cells and Microscopy', /microscop|cell organelles|plant and animal cells|animal and plant cells/],
  ['8', 'Biological Sciences', 'Plant and Animal Systems', /digestive system|blood vessels|gas exchange|respiratory system|circulatory system/],
  ['8', 'Earth and Space Sciences', 'Rocks, Minerals and the Rock Cycle', /rock cycle|sedimentary rocks|igneous rocks|metamorphic rocks/],
  ['8', 'Earth and Space Sciences', 'Plate Tectonics and Geological Activity', /plate tectonics|plate boundaries|continental drift/],
  ['8', 'Physical Sciences', 'Energy Transfers and Transformations', /heat transfer|convection|energy transfers?|energy transformations?/],
  ['9', 'Chemical Sciences', 'Atomic Structure, Periodic Table and Formulae', /periodic table|atomic structure|polyatomic ions|electron arrangement/],
  ['8', 'Physical Sciences', 'Electrical Circuits', /electric(?:al)? circuits?|parallel and series circuits|series and parallel circuits/],
  ['9', 'Physical Sciences', 'Light, Sound and Waves', /reflection of light|refraction|sound waves|light and sound/],
  ['9', 'Biological Sciences', 'Adaptations and Responses', /structural adaptations|behavioural adaptations|tropisms?|endotherms?|ectotherms?/],
  ['9', 'Earth and Space Sciences', 'Global Systems and Climate Change', /greenhouse effect|keeling curve|climate change|carbon cycle/],
  ['10', 'Chemical Sciences', 'Patterns of Chemical Reactions', /rates? of reactions?|reaction rates?|neutralisation|acids and bases|combustion/],
  ['10', 'Biological Sciences', 'DNA, Cell Division and Inheritance', /punnett|pedigrees?|mitosis|meiosis|cell division|genetic variation|genes and alleles|genotyp|phenotyp|genetic code|\bdna\b|inheritance|mendel/],
  ['10', 'Biological Sciences', 'Evolution and Natural Selection', /natural selection|evidence for evolution|speciation/],
  ['10', 'Physical Sciences', 'Motion and Newtons Laws', /newton.?s laws|speed.time graphs?|distance.time graphs?|acceleration|kinetic energy|motion review/],
  ['10', 'Earth and Space Sciences', 'Stars, Galaxies and the Universe', /big bang|galaxies|stellar|life cycle of stars|cosmic microwave|red[ -]?shift/],
];
const clearJuniorTopics = /\b(?:simple machines?|dichotomous keys?|phases of the moon|eclipses?|rock cycle|plate tectonics|electrical circuits?|electric circuits?|series and parallel circuits|parallel and series circuits|sound waves|rates? of reactions?|reaction rates?|mitosis|meiosis|cell division|punnett squares?|newton.?s laws|big bang|cosmic microwave)\b/;
const chapterPlacements = [
  [/^science 1\.1 mechanics/i, '10', 'Physical Sciences', 'Motion and Newtons Laws'],
  [/^science 1\.5 acids and bases/i, '10', 'Chemical Sciences', 'Patterns of Chemical Reactions'],
  [/^science 1\.9 genetic variation/i, '10', 'Biological Sciences', 'DNA, Cell Division and Inheritance'],
  [/^physics [12]\.[34] waves/i, '11', 'Physical Sciences', 'Waves'],
  [/^physics 1\.5 heat/i, '11', 'Physical Sciences', 'Heating and Energy Transfers'],
  [/^chemistry 3\.6.*aqueous equilibrium/i, '12', 'Chemical Sciences', 'Equilibrium and Acids and Bases'],
  [/^biology 2\.4.*cells/i, '11', 'Biological Sciences', 'Cells and Multicellular Organisms'],
  [/^biology 3\.5.*evolution/i, '12', 'Biological Sciences', 'Inheritance and Evolution'],
];
const courseStrands = { Chemistry: 'Chemical Sciences', Physics: 'Physical Sciences', Biology: 'Biological Sciences' };

export function worksheetYears(row) {
  const input = row.years?.length ? row.years : [row.year];
  return [...new Set(input.flatMap(value => {
    const match = String(value || '').trim().match(/^(?:years?\s+)?(\d{1,2})(?:\s*[-–—]\s*(\d{1,2}))?$/i);
    if (!match) return [];
    const start = Number(match[1]), end = Number(match[2] || start);
    return start >= 1 && end <= 12 && end >= start
      ? Array.from({ length: end - start + 1 }, (_, index) => String(start + index)) : [];
  }))].sort((a, b) => Number(a) - Number(b));
}

function cleanTitle(value) {
  const title = String(value || '').replace(/\.(?:pdf|docx?|pptx?|xlsx?)$/i, '')
    .replace(/^[\s_–—-]+|[\s_–—-]+$/g, '').replace(/\s+/g, ' ').replace(/\s+([,.;?!])/g, '$1').trim();
  const corrected = title.replace(/\bp\s*h\s*et\b/gi, 'PhET')
    .replace(/\bph\b/gi, 'pH').replace(/\bpoh\b/gi, 'pOH').replace(/[,;]+$/, '')
    .replace(/\p{L}{6,}/gu, word => /[a-z][A-Z].*[a-z][A-Z]/.test(word) ? word.toLowerCase() : word);
  return /^(?:pH|pOH)\b/.test(corrected) ? corrected : corrected.charAt(0).toUpperCase() + corrected.slice(1);
}

export function organiseWorksheets(rows) {
  const topicYears = new Map();
  for (const row of rows) {
    const years = worksheetYears(row);
    const topic = row.supportingTopic || row.topic;
    if (years.length !== 1 || !topic || placeholder.test(topic)) continue;
    const key = [row.subject, topic.toLowerCase()].join('|');
    const evidence = topicYears.get(key) || new Map();
    evidence.set(years[0], (evidence.get(years[0]) || 0) + 1);
    topicYears.set(key, evidence);
  }
  return rows.map(row => {
    const source = row.originalFilename || row.worksheet?.name || '';
    const title = cleanTitle(row.title) || cleanTitle(source.replace(/^\d+\s*[-–]\s*/, '')) || 'Worksheet';
    let years = worksheetYears(row);
    let topic = row.supportingTopic || row.topic || '';
    let strand = row.strand;
    const subject = row.subject;
    const titleText = title.toLowerCase();
    const evidence = topicYears.get([subject, topic.toLowerCase()].join('|'));
    const path = String(row.id || '');
    const explicitYear = path.match(/(?:^|\/)year[ -](\d{1,2})(?=\/| - | book \d)/i)?.[1];
    const sourceChapter = path.match(/\/scipad\/([^/]+)\//i)?.[1] || '';
    const chapter = chapterPlacements.find(([pattern]) => pattern.test(sourceChapter));
    const junior = subject === 'Science' && juniorScience.find(([, , , pattern]) => pattern.test(titleText));
    const course = senior.find(([name, , , pattern]) => name === subject && pattern.test(titleText));
    if (junior && clearJuniorTopics.test(titleText) && years.every(year => Number(year) <= 10)) {
      years = [junior[0]];
      [, strand, topic] = junior;
    } else if (years.length !== 1) {
      const eligible = year => !years.length || years.includes(year);
      const likelyYear = evidence?.size === 1 && [...evidence].find(([, count]) => count >= 3)?.[0];
      if (explicitYear && Number(explicitYear) >= 1 && Number(explicitYear) <= 12 && eligible(explicitYear)) {
        years = [explicitYear];
      } else if (junior && eligible(junior[0]) && (!topic || placeholder.test(topic) || !years.length)) {
        years = [junior[0]];
        [, strand, topic] = junior;
      } else if (course && eligible(course[1]) && (!years.length || placeholder.test(topic))) {
        years = [course[1]];
        topic = course[2];
        strand = courseStrands[subject];
      } else if (chapter && eligible(chapter[1])) {
        years = [chapter[1]];
        [, , strand, topic] = chapter;
      } else if (likelyYear && eligible(likelyYear)) {
        years = [likelyYear];
      }
    }
    if (!years.length && /^level [23] (?:biology|chemistry|physics)\b/i.test(sourceChapter)) {
      years = ['11', '12'];
    }
    if ((!topic || placeholder.test(topic)) && course && years.includes(course[1])) {
      topic = course[2];
      strand = courseStrands[subject];
    }
    if (!topic || placeholder.test(topic)) {
      topic = title === 'Worksheet' || placeholder.test(title) ? 'Topic to review' : title;
    }
    const name = /^(?:(?:end of )?chapter (?:review|summary|crossword)|practice exam|review questions|key terms)\b/i.test(title)
      && topic !== title && topic !== 'Topic to review' && !title.toLowerCase().includes(topic.toLowerCase())
      ? topic + ' – ' + title : title;
    const extension = source.match(/\.[a-z0-9]+$/i)?.[0] || '';
    const worksheet = row.worksheet && { ...row.worksheet, name: name.replace(/[<>:"/\\|?*]/g, ' – ') + extension };
    return { ...row, title: name, worksheet, year: years.length > 1 ? years[0] + '–' + years.at(-1) : years[0] || '',
      years, strand, topic, supportingTopic: topic };
  });
}

const stopWords = new Set(['a', 'an', 'and', 'by', 'for', 'in', 'of', 'on', 'the', 'to', 'with']);
const tokens = value => String(value || '').normalize('NFKD').toLowerCase()
  .replace(/\bred[ -]shift\b/g, 'redshift').replace(/\bblue[ -]shift\b/g, 'blueshift')
  .replace(/\bp\s*h\s*et\b/g, 'phet').replace(/\p{M}|['’]/gu, '')
  .match(/[\p{L}\p{N}]+/gu) || [];
function stem(word) {
  if (word.length > 5 && word.endsWith('ies')) return word.slice(0, -3) + 'y';
  return word.length >= 4 && /[^saoui]s$/.test(word) ? word.slice(0, -1) : word;
}
const indexes = new WeakMap();
function searchIndex(row) {
  if (indexes.has(row)) return indexes.get(row);
  const fields = [
    [row.title, 12],
    [[row.topic, row.supportingTopic, row.strand, row.subject, row.school, row.area].filter(Boolean).join(' '), 7],
    [[row.publisher, row.publisherCategory, row.originalFilename, row.format, row.role, row.resourceType, ...(row.resourceTypes || [])].filter(Boolean).join(' '), 4],
    [[...(Array.isArray(row.keywords) ? row.keywords : [row.keywords]), row.description, row.searchText].filter(Boolean).join(' '), 1],
  ].map(([text, weight]) => {
    const words = tokens(text).filter(word => !stopWords.has(word)).map(stem);
    return { phrase: ' ' + words.join(' ') + ' ', words: new Set(words), weight };
  });
  indexes.set(row, fields);
  return fields;
}

export function worksheetQuery(value) {
  const years = [];
  const text = value.replace(/\b(?:year|yr)\s*(\d{1,2})\b/gi, (_, year) => { years.push(year); return ' '; });
  const words = tokens(text).filter(word => !stopWords.has(word)).map(stem);
  return { years, words, active: Boolean(years.length || words.length) };
}

export function worksheetScore(row, query) {
  if (query.years.some(year => !worksheetYears(row).includes(year))) return -1;
  if (!query.words.length) return 0;
  const fields = searchIndex(row);
  const weights = query.words.map(word => fields.find(field => field.words.has(word))?.weight || 0);
  if (weights.includes(0)) return -1;
  const phrase = ' ' + query.words.join(' ') + ' ';
  const match = fields.find(field => field.phrase.includes(phrase));
  if (!match && weights.every(weight => weight === 1)) return -1;
  return weights.reduce((sum, weight) => sum + weight, 0) + (match?.weight || 0) * 3
    + (fields[0].phrase === phrase ? 40 : 0);
}
