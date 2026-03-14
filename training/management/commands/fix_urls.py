"""One-time command to fix broken Wikimedia image URLs."""
from django.core.management.base import BaseCommand
from training.models import Artwork


# Mapping of catalog_id → corrected wikimedia_url
URL_FIXES = {
    # F1 — Phase 1
    'F1-01': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Malevich.black-square.jpg/600px-Malevich.black-square.jpg',
    'F1-02': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Kazimir_Malevich_-_%27Suprematist_Composition-_White_on_White%27%2C_oil_on_canvas%2C_1918%2C_Museum_of_Modern_Art.jpg/600px-Kazimir_Malevich_-_%27Suprematist_Composition-_White_on_White%27%2C_oil_on_canvas%2C_1918%2C_Museum_of_Modern_Art.jpg',
    'F1-04': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Piet_Mondriaan%2C_1930_-_Mondrian_Composition_II_in_Red%2C_Blue%2C_and_Yellow.jpg/600px-Piet_Mondriaan%2C_1930_-_Mondrian_Composition_II_in_Red%2C_Blue%2C_and_Yellow.jpg',
    'F1-05': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Tableau_I%2C_by_Piet_Mondriaan.jpg/600px-Tableau_I%2C_by_Piet_Mondriaan.jpg',
    'F1-06': 'https://upload.wikimedia.org/wikipedia/commons/2/28/Kelly_%E2%80%93_Red_Blue_Green.jpg',
    'F1-08': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Josef_Albers%27_Studies_for_Homage_to_the_Square.jpg/600px-Josef_Albers%27_Studies_for_Homage_to_the_Square.jpg',

    # F2 — Phase 2
    'F2-03': 'https://upload.wikimedia.org/wikipedia/en/1/1b/Riley%2C_Movement_in_Squares.jpg',
    'F2-06': 'https://upload.wikimedia.org/wikipedia/en/4/4c/Sky_and_Water_I.jpg',

    # F3 — Phase 3
    'F3-01': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Francisco_de_Zurbar%C3%A1n_-_Still-life_with_Lemons%2C_Oranges_and_Rose_-_WGA26062.jpg/800px-Francisco_de_Zurbar%C3%A1n_-_Still-life_with_Lemons%2C_Oranges_and_Rose_-_WGA26062.jpg',
    'F3-02': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Francisco_de_Zurbar%C3%A1n_-_Agnus_Dei_-_Google_Art_Project.jpg/800px-Francisco_de_Zurbar%C3%A1n_-_Agnus_Dei_-_Google_Art_Project.jpg',
    'F3-03': 'https://upload.wikimedia.org/wikipedia/en/6/67/%27Natura_Morta%27%2C_oil_on_canvas_painting_by_Giorgio_Morandi%2C_1956%2C_private_collection.jpg',
    'F3-05': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Jean-Sim%C3%A9on_Chardin_%28French_-_Still_Life_with_Peaches%2C_a_Silver_Goblet%2C_Grapes%2C_and_Walnuts_-_Google_Art_Project.jpg/600px-Jean-Sim%C3%A9on_Chardin_%28French_-_Still_Life_with_Peaches%2C_a_Silver_Goblet%2C_Grapes%2C_and_Walnuts_-_Google_Art_Project.jpg',

    # F4 — Phase 4 (Hopper + de Chirico)
    'F4-01': 'https://upload.wikimedia.org/wikipedia/en/e/e7/Sun_in_an_Empty_Room_1963.jpg',
    'F4-02': 'https://upload.wikimedia.org/wikipedia/en/a/aa/Rooms_by_the_Sea_1951.jpg',
    'F4-03': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Edward_Hopper_-_Morning_Sun_-_c_1952_-_Columbus_Museum_of_Art.jpg/800px-Edward_Hopper_-_Morning_Sun_-_c_1952_-_Columbus_Museum_of_Art.jpg',
    'F4-04': 'https://upload.wikimedia.org/wikipedia/en/d/df/The_Disquieting_Muses.jpg',
    'F4-05': 'https://upload.wikimedia.org/wikipedia/en/6/68/The_Enigma_of_the_Hour.jpg',

    # F5 — Phase 5
    'F5-01': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Tsunami_by_hokusai_19th_century.jpg/800px-Tsunami_by_hokusai_19th_century.jpg',
    'F5-02': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Katsushika_Hokusai%2C_published_by_Nishimuraya_Yohachi_%28Eijud%C5%8D%29_-_Fine_Wind%2C_Clear_Weather_%28Gaif%C5%AB_kaisei%29_-_Google_Art_Project.jpg/800px-Katsushika_Hokusai%2C_published_by_Nishimuraya_Yohachi_%28Eijud%C5%8D%29_-_Fine_Wind%2C_Clear_Weather_%28Gaif%C5%AB_kaisei%29_-_Google_Art_Project.jpg',
    'F5-03': 'https://upload.wikimedia.org/wikipedia/en/0/07/Jimson_Weed_by_Georgia_O%27Keeffe.jpg',
    'F5-04': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Georgia_O%27Keeffe_Red_Canna_1919_HMA.jpg/500px-Georgia_O%27Keeffe_Red_Canna_1919_HMA.jpg',
    'F5-05': 'https://upload.wikimedia.org/wikipedia/en/b/b7/Georgia_O%27Keeffe%2C_Black_Iris%2C_1926%2C_Metropolitan_Museum_of_Art.jpg',

    # F6 — Phase 6
    'F6-01': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Meisje_met_de_parel.jpg/600px-Meisje_met_de_parel.jpg',
    'F6-02': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Johannes_Vermeer_-_Het_melkmeisje_-_Google_Art_Project.jpg/600px-Johannes_Vermeer_-_Het_melkmeisje_-_Google_Art_Project.jpg',
    'F6-03': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Jan_Vermeer_-_The_Art_of_Painting_-_Google_Art_Project.jpg/600px-Jan_Vermeer_-_The_Art_of_Painting_-_Google_Art_Project.jpg',
    'F6-04': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Turner_-_Rain%2C_Steam_and_Speed_-_National_Gallery_file.jpg/800px-Turner_-_Rain%2C_Steam_and_Speed_-_National_Gallery_file.jpg',
    'F6-05': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/The_Fighting_Temeraire%2C_JMW_Turner%2C_National_Gallery.jpg/800px-The_Fighting_Temeraire%2C_JMW_Turner%2C_National_Gallery.jpg',
    'F6-06': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Joseph_Mallord_William_Turner_-_Snow_Storm_-_Steam-Boat_off_a_Harbour%27s_Mouth_-_WGA23178.jpg/800px-Joseph_Mallord_William_Turner_-_Snow_Storm_-_Steam-Boat_off_a_Harbour%27s_Mouth_-_WGA23178.jpg',

    # Artworks whose exact painting is not on Wikimedia — using closest available substitute
    # F1-03: Eight Red Rectangles → Suprematism by Malevich (same artist/period, similar geometric composition)
    'F1-03': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Kazimir_Malevich_-_Suprematism_-_Google_Art_Project.jpg/600px-Kazimir_Malevich_-_Suprematism_-_Google_Art_Project.jpg',
    # F1-07: Kelly Blue Green Red I → Kelly sculpture/installation (same artist, color field work)
    'F1-07': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/EKelly-V3.jpg/600px-EKelly-V3.jpg',
    # F2-01: Vasarely Vega-Nor → Vasarely Supernovae (same artist, same op-art sphere style)
    'F2-01': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Supernovae_%281959-61%29_by_Victor_Vasarely.jpg/600px-Supernovae_%281959-61%29_by_Victor_Vasarely.jpg',
    # F2-02: Vasarely Zebegen → Vasarely Tribute to Malevitch (same artist, op-art)
    'F2-02': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Victor_Vasarely_%2828Tribute_to_Malevitch%29_UCV_1954.jpg/600px-Victor_Vasarely_%2828Tribute_to_Malevitch%29_UCV_1954.jpg',
    # F2-04: Riley Fall → Riley Shadowplay (same artist, op-art B&W)
    'F2-04': 'https://upload.wikimedia.org/wikipedia/en/7/7c/Riley%2C_Shadowplay.jpg',
    # F2-05: Riley Blaze → Riley Bolt of Colour (same artist, colorful radiating pattern)
    'F2-05': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Bridget-riley-bolt-of-colour-1-chinati-foundatin-marfa-texas.jpg/600px-Bridget-riley-bolt-of-colour-1-chinati-foundatin-marfa-texas.jpg',
    # F3-04: Morandi Still Life 1946 → Morandi Natura Morta 1956 (same artist, same subject)
    'F3-04': 'https://upload.wikimedia.org/wikipedia/en/6/67/%27Natura_Morta%27%2C_oil_on_canvas_painting_by_Giorgio_Morandi%2C_1956%2C_private_collection.jpg',
    # F4-06: de Chirico Piazza d'Italia → de Chirico The Red Tower (same artist, metaphysical period)
    'F4-06': 'https://upload.wikimedia.org/wikipedia/en/b/b2/The_Red_Tower_by_Giorgio_de_Chirico.jpg',
}


class Command(BaseCommand):
    help = 'Fixes broken Wikimedia image URLs in the database'

    def handle(self, *args, **options):
        updated = 0
        for catalog_id, new_url in URL_FIXES.items():
            try:
                artwork = Artwork.objects.get(catalog_id=catalog_id)
                if artwork.wikimedia_url != new_url:
                    old = artwork.wikimedia_url[:80]
                    artwork.wikimedia_url = new_url
                    artwork.save(update_fields=['wikimedia_url'])
                    self.stdout.write(f'  ✓ {catalog_id}: updated')
                    updated += 1
                else:
                    self.stdout.write(f'  - {catalog_id}: already correct')
            except Artwork.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  ! {catalog_id}: not found'))

        self.stdout.write(f'\nUpdated {updated} URLs.')
