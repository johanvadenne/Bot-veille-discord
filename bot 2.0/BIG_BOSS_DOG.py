# import
import discord
import fonction_generale
import flux_rss
import page_liens
import pprint
from discord.ext import commands

# init
test_historique = []

class BIG_BOSS_DOG(commands.Bot):

    # init
    premier_message = True
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.salons = {}
        self.utilisateur_principal = None
        self.analyse = True

    def salon(self):

        # FR: connexion au serveur
        # EN: server connection
        guild = self.get_guild("ID_SERVER")
        
        # FR: récupère tout les noms des salons discord
        # EN: get all the names of discord lounges
        if guild is not None:
            for channel in guild.channels:
                nom = channel.name
                if "-" in nom:
                    nom = channel.name.split("-", 1)[1]
                self.salons[nom] = channel.id
            pprint.pprint(self.salons)
        
        # FR: vérifie si les catégories des flux rss sont existant dans le serveur
        # EN: checks whether rss feed categories exist in the server
        for site in flux_rss.flux_rss:
            for nom_site, liens_rss in site.items():
                if nom_site not in self.salons:
                    print(nom_site+" - NO")
                    self.analyse = False
                for lien, categorie in liens_rss.items():
                    if categorie not in self.salons:
                        print(categorie+" - NO")
                        self.analyse = False
        
        # FR: vérifie si les catégories des sites sont existant dans le serveur
        # EN: checks whether site categories exist in the server
        for site in page_liens.sites:
            for nom_site, liens in site.items():
                if nom_site not in self.salons:
                    print(nom_site+" - NO")
                    self.analyse = False
                for lien, categorie in liens.items():
                    if categorie not in self.salons:
                        print(categorie+" - NO")
                        self.analyse = False

    

    # FR: fonction qui cherche et envoie les actualités
    # EN: function that searches for and sends news
    async def recherche_actus_url(self):
        if self.analyse:
            
            # FR: envoie un gif de confirmation d'execution de la commande
            # EN: sends an order confirmation gif
            if self.utilisateur_principal:
                await self.utilisateur_principal.send("https://tenor.com/view/jim-carrey-bruce-almighty-typing-gif-3547478")

            
            # FR: récupère les nouvelles actualités
            # EN: recovers current news
            fonction_generale.lecture_fichieru_url(self.salons)

            # FR: envoie le nombre d'actualités trouvée
            # EN: sends the number of updates found
            if self.utilisateur_principal:
                rapport = "rapport:\nnouvelles actualités: "+str(len(fonction_generale.nouvelles_actus))
                await self.utilisateur_principal.send(rapport)
            
            # FR: enregistre les nouvelles actualités dans un fichier historique
            # EN: saves new updates in a history file
            fichier_historique = open(r".\historique.py", "w+", encoding="utf-8")
            fichier_historique.write("historique="+str(fonction_generale.historique.historique))
            fichier_historique.close()

            # FR: envoie les nouvelles actualités dans les trois canaux dédié aux liens
            # EN: sends news to the three dedicated link channels
            for lien, categories in fonction_generale.nouvelles_actus.items():

                id_all = self.salons["all"]
                id_site = categories[0]
                id_categ = categories[1]
                print(lien)

                # channels all
                salon = Big_Boss_Dog.get_channel(id_all)
                if salon:
                    await salon.send(str(lien))

                # channels site
                salon = Big_Boss_Dog.get_channel(id_site)
                if salon:
                    await salon.send(str(lien))

                # channels category
                salon = Big_Boss_Dog.get_channel(id_categ)
                if salon:
                    await salon.send(str(lien))
        
            
            # FR: envoie la confirmation de son travail terminé
            # EN: sends confirmation of completed work
            if self.utilisateur_principal:
                await self.utilisateur_principal.send("https://tenor.com/view/finished-spongebob-squarepantes-spongebob-squarepants-dusting-gif-5894625")
                
        else:
            # FR: envoie une erreur
            # EN: sends error
            if self.utilisateur_principal:
                await self.utilisateur_principal.send("https://tenor.com/view/dog-computer-gif-14860983")
                    
    
    # FR: fonction qui cherche et envoie les actualités
    # EN: function that searches for and sends news
    async def recherche_actus_rss(self):
        if self.analyse:
            # FR: envoie un gif de confirmation d'execution de la commande
            # EN: sends an order confirmation gif
            if self.utilisateur_principal:
                await self.utilisateur_principal.send("https://tenor.com/view/jim-carrey-bruce-almighty-typing-gif-3547478")

            # FR: récupère les nouvelles actualités
            # EN: recovers current news
            fonction_generale.lecture_fichier_rss(self.salons)
            
            # FR: envoie le nombre d'actualités trouvée
            # EN: sends the number of updates found
            if self.utilisateur_principal:
                rapport = "rapport:\nnouvelles actualités: "+str(len(fonction_generale.nouvelles_actus))
                await self.utilisateur_principal.send(rapport)
            
            # FR: enregistre les nouvelles actualités dans un fichier historique
            # EN: saves new updates in a history file
            fichier_historique = open("historique.py", "w+", encoding="utf-8")
            fichier_historique.write("historique="+str(fonction_generale.historique.historique))
            fichier_historique.close()

            # FR: envoie les nouvelles actualités dans les trois canaux dédié aux liens
            # EN: sends news to the three dedicated link channels
            for lien, categories in fonction_generale.nouvelles_actus.items():

                id_all = self.salons["all"]
                id_site = categories[0]
                id_categ = categories[1]
                print(lien)

                # channels all
                salon = Big_Boss_Dog.get_channel(id_all)
                if salon:
                    await salon.send(str(lien))

                # channels site
                salon = Big_Boss_Dog.get_channel(id_site)
                if salon:
                    await salon.send(str(lien))

                # channels category
                salon = Big_Boss_Dog.get_channel(id_categ)
                if salon:
                    await salon.send(str(lien))
            
            # FR: envoie la confirmation de son travail terminé
            # EN: sends confirmation of completed work
            if self.utilisateur_principal:
                await self.utilisateur_principal.send("https://tenor.com/view/finished-spongebob-squarepantes-spongebob-squarepants-dusting-gif-5894625")

            # FR: envoie une erreur
            # EN: sends error
        else:
            if self.utilisateur_principal:
                await self.utilisateur_principal.send("https://tenor.com/view/dog-computer-gif-14860983")


    # FR: fonction qui s'enclenche lorsque le bot est prêt
    # EN: function that switches on when the bot is ready
    async def on_ready(self):
        print("BOT prêt")
        print('------')

        ## FR: si un message n'a pas encore été envoyer, alors envoyé un message.
        ## EN: if a message has not yet been sent, then send a message.
        if self.premier_message:
            self.utilisateur_principal = await self.fetch_user("ID_USER")
            if self.utilisateur_principal:
                self.salon()
                await self.utilisateur_principal.send("Je suis prêt!")
                self.premier_message = False



# init
intents = discord.Intents.default()
intents.message_content = True
Big_Boss_Dog = BIG_BOSS_DOG(command_prefix='/', intents=intents)

# command
@Big_Boss_Dog.command()
async def rapporte_rss(ctx):
    await Big_Boss_Dog.recherche_actus_rss()

# command
@Big_Boss_Dog.command()
async def rapporte_url(ctx):
    await Big_Boss_Dog.recherche_actus_url()

# command
@Big_Boss_Dog.command()
async def chao(ctx):
    if Big_Boss_Dog.utilisateur_principal:
        await Big_Boss_Dog.utilisateur_principal.send("https://tenor.com/view/lisa-simpson-chao-adios-ralph-wiggum-gif-13894126")
    await Big_Boss_Dog.close()

@Big_Boss_Dog.event
async def on_message(message):
    if not message.author.bot:
        await Big_Boss_Dog.process_commands(message)

# FR: active le bot
# EN: activate bot
Big_Boss_Dog.run("TOKEN")