class BoatCategory {
  static getCategoryString(b) {
    let boatstr = ''

    if (b.category === 0) {
      boatstr += 'G'
    }

    if (b.coxswain === 0 || b.coxswain === 3) {
      boatstr += (b.crewsize - 1).toString()
    } else {
      boatstr += b.crewsize.toString()
    }

    if (b.discipline === 0 || b.discipline === 2) {
      boatstr += 'x'
    }

    if (b.coxswain === 0 || b.coxswain === 3) {
      boatstr += '+'
    }

    return boatstr
  }

  static getCategories(boats) {
    const categories = {}

    boats.forEach((boat, i) => {
      categories[boat.uuid] = this.getCategoryString(boat)
    })

    return categories
  }
}

const Categories = {
  'racing': 1,
  'gig': 0
}

const Coxswain = {
  'standardwithoutcox': 4,
  'standardwithcox': 3,
  'changeablecox': 2,
  'withoutcox': 1,
  'withcox': 0
}

const Disciplines = {
  'standardsculling': 2,
  'standardsweep': 3,
  'sculling': 0,
  'sweep': 1,
  'unknown': 4
}


export {
  BoatCategory,
  Categories,
  Coxswain,
  Disciplines
}
