from core.db.session import session
from app.paciente.dto.paciente_coordenadas import PacienteCoordenadas
from api.paciente.v1.request.paciente_coordenadas_request import PacienteCoordenadasLote
from app.paciente.services import coordenadas
from distutils import log
from app.paciente.services.coordenadas_validacao import validacao
async def service_atualiza_paciente_coordenadas_lote(pacienteCoordenadasLote: PacienteCoordenadasLote):

    sql = """
            select max(p.id), 
                   CASE
                        WHEN et.endereco_tratado IS NOT NULL THEN et.endereco_tratado
                        ELSE CONCAT(p.DS_ENDERECO, ', ', p.NR_ENDERECO, ', ', p.NM_BAIRRO, ' - SP')
                   END AS endereco_final
              from paciente p
          left join endereco_tratado et on p.CD_ATENDIMENTO = et.CD_ATENDIMENTO
              where not exists (select 1
                                  from paciente_coordenadas pc
                                 where pc.id_paciente = p.ID
                                   and (pc.validado = 1 or pc.provider = :provider) )
                and YEAR(STR_TO_DATE(DT_ATENDIMENTO, '%Y-%m-%d')) = :ano
              group by endereco_final
              order by 1 asc
              limit :limit;
            """
    pacientes = (await session.execute(sql, pacienteCoordenadasLote.to_dict())).all()
    dados_coordenadas_lista = []
    for paciente in pacientes:
        id_paciente = paciente[0]
        endereco = paciente[1]
        response = {'endereco': endereco, 'provider': pacienteCoordenadasLote.provider, 'id_paciente': id_paciente}
        paciente_coordenadas = PacienteCoordenadas.parse_obj(response)
        try:
            dados_coordenadas = coordenadas.execute(endereco, pacienteCoordenadasLote.provider)
            response.update(dados_coordenadas)
            response.update(validacao(pacienteCoordenadasLote.provider, response))
            paciente_coordenadas = PacienteCoordenadas.parse_obj(response)
        except Exception as ex:
            mensagem_erro = f"Não foi possível obter coordenadas {id_paciente}, erro: {ex}"
            log.error(mensagem_erro)
            paciente_coordenadas.response=mensagem_erro

        inserir_sql = """
                        INSERT INTO paciente_coordenadas (id_paciente, endereco, latitude, longitude, x, y, acuracia, provider, response, postcode, city, state, 
                                                          country, county, quarter, suburb, formatted, validado, data_criacao, data_alteracao)
                        VALUES (:id_paciente, :endereco, :latitude, :longitude, :x, :y, :acuracia, :provider, :response, 
                                :postcode, :city, :state, :country, :county, :quarter, :suburb, :formatted, :validado, NOW(), NOW())
                      """
        await session.execute(inserir_sql, paciente_coordenadas.dict())
        await session.commit()

        dados_coordenadas_lista.append(response)
    return dados_coordenadas_lista
