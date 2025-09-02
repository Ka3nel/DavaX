BOOK_SUMMARIES = {
    "The Hobbit": "Bilbo Baggins joins dwarves to reclaim treasure from Smaug; along the way he discovers courage and cunning, meets trolls, goblins, elves, and finds a mysterious ring.",
    "1984": "Winston Smith rebels against a surveillance state led by Big Brother, seeking truth and love against overwhelming propaganda and control.",
    "To Kill a Mockingbird": "Through Scout Finch’s eyes, the novel examines racial injustice and moral growth as Atticus Finch defends Tom Robinson.",
    "Pride and Prejudice": "Elizabeth Bennet navigates class, family, and love as she clashes with—and grows to understand—Mr. Darcy.",
    "Harry Potter and the Sorcerer’s Stone": "Harry discovers he is a wizard, attends Hogwarts, forms friendships, and faces the shadow of Voldemort.",
    "The Great Gatsby": "A portrait of Jazz Age longing and illusion centered on Jay Gatsby’s obsession with Daisy Buchanan.",
    "The Catcher in the Rye": "Holden Caulfield wanders New York wrestling with alienation, grief, and the desire to protect innocence.",
    "The Fellowship of the Ring": "Frodo begins the quest to destroy the One Ring with a fellowship sworn against Sauron.",
    "Animal Farm": "Animals oust humans but pigs gradually establish tyranny, critiquing power and revolution.",
    "Brave New World": "Engineered comfort and control suppress individuality in a technocratic society.",
    "The Little Prince": "A fable about love, responsibility, and seeing with the heart."
}

def get_summary_by_title(title: str) -> str:
    return BOOK_SUMMARIES.get(title, "No detailed summary found for this title.")
