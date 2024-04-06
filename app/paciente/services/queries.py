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
        SELECT count(1) qtd, concat(CD_CID, '-',DS_CID) cid
         FROM paciente
        WHERE dt_atendimento BETWEEN STR_TO_DATE(:dt_inicial, '%d%m%Y') AND STR_TO_DATE(:dt_final, '%d%m%Y')
     GROUP BY concat(CD_CID, '-',DS_CID)
     ORDER BY concat(CD_CID, '-',DS_CID);
    """

def query_agrupado_por_cid_maiores():
    return """
        SELECT count(1) qtd, concat(CD_CID, '-',DS_CID) cid
         FROM paciente
        WHERE dt_atendimento BETWEEN STR_TO_DATE(:dt_inicial, '%d%m%Y') AND STR_TO_DATE(:dt_final, '%d%m%Y')
     GROUP BY concat(CD_CID, '-',DS_CID)
     ORDER BY 1 desc
     limit 10;
    """

def query_agrupado_internacao_alta():
    return """
        SELECT
                a.DT_ALTA,
                COALESCE(qtd_internacao, 0) AS qtd_internacao,
                i.DT_ATENDIMENTO,
                COALESCE(qtd_alta, 0) AS qtd_alta
            FROM
                (SELECT COUNT(1) AS qtd_internacao, DT_ATENDIMENTO
                FROM paciente
                WHERE DT_ATENDIMENTO BETWEEN STR_TO_DATE(:dt_inicial, '%d%m%Y') AND STR_TO_DATE(:dt_final, '%d%m%Y')
                  AND ds_leito IS NOT NULL
                GROUP BY DT_ATENDIMENTO) AS i
            JOIN
                (SELECT COUNT(1) AS qtd_alta, DT_ALTA
                FROM paciente
                WHERE DT_ALTA BETWEEN STR_TO_DATE(:dt_inicial, '%d%m%Y') AND STR_TO_DATE(:dt_final, '%d%m%Y')
                  AND ds_leito IS NOT NULL
                GROUP BY DT_ALTA) AS a
            ON i.DT_ATENDIMENTO = a.DT_ALTA
            ORDER BY i.DT_ATENDIMENTO, a.DT_ALTA;
    """


def query_factory(query):
    query_mappings = {
        'dia': query_agrupado_dia,
        'mes': query_agrupado_mes,
        'cid': query_agrupado_por_cid,
        'cid_maiores': query_agrupado_por_cid_maiores,
        'internacao_alta': query_agrupado_internacao_alta,
    }
    return query_mappings.get(query.lower(), query_agrupado_dia)()
