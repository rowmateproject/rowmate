class BoatCategory {
  static getCategoryString(b) {
    let boatstr = ""
    if (b.category == 0) {
      boatstr += "G"
    }
    if (b.coxswain === 0 || b.coxswain === 3) {
      boatstr += (b.crewsize-1).toString()
    } else {
      boatstr += b.crewsize.toString()
    }

    if (b.discipline == 0 || b.discipline == 2) {
      boatstr += "x"
    }

    if (b.coxswain == 0 || b.coxswain == 3) {
      boatstr += "+"
    }




    return boatstr
  }
  static getCategories(boats) {
    let categories = {}
    boats.forEach((boat, i) => {
      categories[boat.id] = this.getCategoryString(boat)
    });

    return categories
  }
}

export {
  BoatCategory
}
