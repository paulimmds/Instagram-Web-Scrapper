from bot import *

bot = Bot()

bot.open_driver()

choice = 0

while choice != '4' :
    print("O que você deseja fazer?")
    print("1 - Hashtags Posts")
    print("2 - Commented Posts")
    print("3 - Tagged Posts")
    print("4 - Finalizar execução")
    choice = input("Insira sua resposta : ")

    if choice == '1':
        hashtags = input("Insira as hashtags que você deseja pesquisar, separado por vírgula: ")
        hashtags = hashtags.split(',')
        hashtags = [str("https://www.instagram.com/explore/tags/"+str(hashtag)+"/") for hashtag in hashtags]
        limite_post = int(input("Digite o número de posts que você deseja raspar em cada hashtag: "))
        for hashtag in hashtags:
            bot.driver.get(hashtag)
            sleep(3)
            bot.hashtags_posts(hashtag, limite_post)
            nome_arquivo = f"{hashtag[38:].replace('/','')}-hashtag-posts.csv"
            for url in bot.profileUrl:
                bot.coleta_dados(url)
                bot.importar(nome_arquivo, url)
            bot.set_variables()

    elif choice == '2':
        links = input("Insira os usuários, separado por vírgula: ")
        links = links.split(',')
        links = [str("https://www.instagram.com/"+str(link)+"/") for link in links]
        limite_post = int(input("Digite o número de posts que você deseja raspar em cada perfil: "))
        limite_user = int(input("Digite o número de usuários que você deseja raspar em cada post: "))
        for link in links:
            bot.driver.get(link)
            sleep(3)
            bot.commented_posts(link,limite_post,limite_user)
            nome_arquivo = f"{link[25:].replace('/','')}-commented-users.csv"
            for url in bot.profileUrl:
                bot.coleta_dados(url)
                bot.importar(nome_arquivo,url)
            bot.set_variables()

    elif choice == '3':
        links = input("Insira os usuários, separado por vírgula: ")
        links = links.split(',')
        links = [str("https://www.instagram.com/"+str(link)+"/") for link in links]
        limite = int(input("Digite o número de posts que você deseja raspar em cada perfil: "))
        for link in links:
            bot.driver.get(link)
            sleep(3)
            bot.tagged_posts(link,limite)
            nome_arquivo = f"{link[25:].replace('/','')}-tagged.csv"
            for url in bot.profileUrl:
                bot.coleta_dados(url)
                bot.importar(nome_arquivo,url)
            bot.set_variables()
        
    elif choice == '4':
        print("Trabalho finalizado!")
        bot.driver.quit()