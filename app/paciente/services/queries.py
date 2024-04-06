def query_agrupado_dia():
    return """
        SELECT count(1) qtd, DT_ATENDIMENTO
          FROM paciente
         WHERE dt_atendimento BETWEEN STR_TO_DATE(:dt_inicial, '%d%m%Y') AND STR_TO_DATE(:dt_final, '%d%m%Y')
      group by DT_ATENDIMENTO
      order by DT_ATENDIMENTO;
    """

def query_agrupado_mes():
    return """
        SELECT count(1) qtd, MONTH(DT_ATENDIMENTO) as "mes"
          FROM paciente
         WHERE dt_atendimento BETWEEN STR_TO_DATE(:dt_inicial, '%d%m%Y') AND STR_TO_DATE(:dt_final, '%d%m%Y')
      group by MONTH(DT_ATENDIMENTO)
      order by MONTH(DT_ATENDIMENTO);
    """

def query_agrupado_por_cid():
    return """
        SELECT count(1) qtd, concat(CD_CID, '-',DS_CID)
         FROM paciente
        WHERE dt_atendimento BETWEEN STR_TO_DATE(:dt_inicial, '%d%m%Y') AND STR_TO_DATE(:dt_final, '%d%m%Y')
     GROUP BY concat(CD_CID, '-',DS_CID)
     ORDER BY concat(CD_CID, '-',DS_CID);
    """

def query_factory(query):
    query_mappings = {
        'dia': query_agrupado_dia,
        'mes': query_agrupado_mes,
        'cid': query_agrupado_por_cid,
    }
    return query_mappings.get(query.lower(), query_agrupado_dia)()
