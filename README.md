<p align="center">
  <img src="https://github.com/juliarobaina/Meu-Coeficiente-De-Rendimento/blob/main/img/logo-3.png" width="90" height="90"/>
</p>

# Qual é o meu CR?
  <p>Este repositório contém os arquivos do Software <b>Qual é o meu CR?</b>. Nesse programa é possível:</p>

  <ul>
    <li>Calcular o Coeficiente de Rendimento Atual;</li>
    <li>Calcular o Coeficiente de Rendimento até um período determinado;</li>
    <li>Simular o Coeficiente de Rendimento com notas digitadas pelo usuário.</li>
  </ul>
  
## Visão Geral
  <p><b>Qual é o meu CR?</b> utiliza o histórico escolar da Universidade Federal Rural do Rio de Janeiro (UFRRJ), gerado pelo Sistema Integrado de Gestão de Atividades Acadêmicas (SIGAA), para realizar as opções descritas acima.</p>
  
## Bibliotecas Necessárias
  <ul>
    <li><a href="https://github.com/camelot-dev/camelot">Camelot: PDF Table Extraction for Humans</a>;</li>
    <li><a href="https://github.com/numpy/numpy">NumPy</a>;</li>
    <li><a href="https://github.com/python-pillow/Pillow">Pillow</a>.</li>
  </ul>

  Você pode instala-las através do comando `pip install -r requirements.txt`
  
## Há duas formas de utilizar o programa no Windows
  <ul>
    <li>Instalando o Ghostscript
        <ol>
          <li><a href="https://www.ghostscript.com/download/gsdnld.html">Baixe e instale o Ghostscript</a>;</li>
          <li>Adicione o caminho da pasta <em>bin</em> e <em>lib</em>, que estão no diretório de instalação dos arquivos do Ghostscript, na variável <em>Path</em> do sistema Windows. Se não souber como fazer isto, veja este artigo de <a href="https://docs.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14)">como adicionar algo no <i>path</i> do Windows</a>.</li>
        </ol>
    </li>
  </ul>
  
## Informações Adicionais
  <p>O usuário deve possuir <a href="https://www.python.org/">Python</a> instalado em seu computador.</p>
  <p>Não foi realizado testes com históricos de outras universidades, portanto, o seu funcionamento não é garantido.</p>



